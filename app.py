from flask import Flask, render_template, request, g, session, redirect, flash, jsonify
from secrets import FLASK_SECRET_KEY
from models import db, connect_db, User, Card
from forms import LoginForm, RegisterForm, CardForm, EditUserForm
from sqlalchemy.exc import IntegrityError
from helpers import handle_image_upload, delete_record_from_s3
from PIL import Image, UnidentifiedImageError
import io

USER_ID = "user_id"

app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cg_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True 

connect_db(app)

db.create_all()

@app.before_request
def add_user_to_g():
    if USER_ID in session:
        g.user = User.query.get(session[USER_ID])
    else:
        g.user = None
        print(request.endpoint)


@app.route('/')
def root_route():
    if g.user:
        return redirect(f'/users/{g.user.id}')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        if user:
            add_user_to_session(user)
            return redirect(f'/users/{user.id}')
        else:
            flash("Incorrect Username or Password")
    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if g.user:
        return redirect(f'/users/{g.user.id}')
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User.register(username=form.username.data,
                                 password=form.password.data,
                                 email = form.email.data,
                                 first_name = form.first_name.data,
                                 last_name = form.last_name.data)
        if new_user:
            db.session.add(new_user)
            try:
                db.session.commit()
                add_user_to_session(new_user)
                flash("User created")
                return redirect(f'/users/{new_user.id}')
            except IntegrityError:
                db.session.rollback()
                flash("Username already taken")
                return redirect('/register')
            except:
                db.session.rollback()
                flash("Error creating user")
                return redirect('/register')
    return render_template('register.html', form=form)

@app.route('/users/<int:id>')
def show_user(id):
    user = User.query.get_or_404(id)
    return render_template('user.html', user=user)

@app.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user_form(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)
    del form.username
    del form.password
    if form.validate_on_submit():
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        try:
            db.session.commit()
            return redirect(f'/users/{user.id}')
        except:
            flash("Changes could not be saved")
            
    return render_template('edit-user.html', user=user, form=form)

@app.route('/users/<int:id>/add_card', methods=['GET', 'POST'])
def add_new_card(id):
    form = CardForm()
    if form.validate_on_submit():
        new_card = Card(owner_id=id,
                        player=form.player.data,
                        year=form.year.data,
                        set_name=form.set_name.data,
                        number=form.number.data,
                        desc=form.desc.data)
        db.session.add(new_card)
        try:
            db.session.commit()
            flash("Card successfully added!")
            if form.image.data:
                try:
                    img = Image.open(request.files[form.image.name])
                    large = (600, 600)
                    img.thumbnail(large)
                    key_stub = f"card_images/{new_card.id}_full"
                    file_key = handle_image_upload(img, key_stub)
                    thumb_key_stub = f"card_images/{new_card.id}_thumb"
                    size = (150, 150)
                    img.thumbnail(size)
                    thumb_file_key = handle_image_upload(img, thumb_key_stub)
                    new_card.img_url = file_key
                    db.session.commit()
                except:
                    flash("Image file is unsupported type")
            return redirect(f'/users/{id}')
        except:
            db.session.rollback()
            flash("Error adding Card")
    return render_template('add-card.html', form=form)

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    try:
        db.session.commit()
        flash("User Deleted!")
        return redirect('/logout')
    except:
        db.session.rollback()
        flash("Error deleting user")
        return redirect("/")

@app.route('/cards')
def show_cards():
    cards = Card.query.all()
    return render_template('cards.html', cards=cards)

@app.route('/cards/<int:id>')
def show_card(id):
    card = Card.query.get_or_404(id)
    return render_template('card.html', card=card)

@app.route('/cards/<int:id>/edit', methods=['GET', 'POST'])
def edit_card(id):
    card = Card.query.get_or_404(id)
    form = CardForm(obj=card)
    if form.validate_on_submit():
        card.player = form.player.data
        card.set_name = form.set_name.data
        card.number = form.number.data
        card.year = form.year.data
        card.desc = form.desc.data
        try:
            db.session.commit()
            flash("Changes saved")
            return redirect(f'/users/{card.user.id}')
        except:
            db.session.rollback()
            flash("error saving changes")
    return render_template('edit-card.html', form=form, card=card)

@app.route('/cards/<int:id>/delete', methods=['POST'])
def delete_card(id):
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    try:
        db.session.commit()
        flash("Card Deleted!")
        if card.img_url: 
            delete_record_from_s3(card)
        return redirect(f'/users/{card.user.id}')
    except:
        db.session.rollback()
        flash('Error deleting card')
        return redirect(request.url)

@app.route('/api/cards')
def get_cards():
    name = request.args.get('name', None)
    cards = []
    if name: 
        cards = Card.query.filter(Card.player.ilike(f'%{name}%'))
    else:
        cards = Card.query.all()
    json = []
    for card in cards:
        json.append(card.serialize())
    return jsonify(results=json)


@app.route('/logout')
def logout_user():
    session.pop(USER_ID)
    flash("Goodbye!")
    return redirect('/')

def add_user_to_session(user):
    session[USER_ID] = user.id