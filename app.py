from flask import Flask, render_template, request, g, session, redirect, flash, jsonify
from secrets import FLASK_SECRET_KEY
from models import db, connect_db, User, Card, TradeRequest, RequestCard
from forms import LoginForm, RegisterForm, CardForm, EditUserForm, TradeRequestForm
from sqlalchemy.exc import IntegrityError
from helpers import handle_image_upload, delete_record_from_s3
from PIL import Image, UnidentifiedImageError
from ebay_api import get_recent_prices
import io
import json
import datetime

USER_ID = "user_id"

app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///cg_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True 

connect_db(app)

@app.before_request
def add_user_to_g():
    """Add authenticated user to flask g"""
    if USER_ID in session:
        g.user = User.query.get(session[USER_ID])
    else:
        g.user = None

########## APP ENTRY ROUTES ##########

@app.route('/index')
def show_index():
    """Show user app entry page"""
    return render_template('index.html')

@app.route('/')
def root_route():
    """Direct authentcated user home or unauthenticated user to show_index route"""
    if g.user:
        return redirect(f'/users/{g.user.id}')
    return redirect('/index')

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Show user the login form.  Handle valid form submission by authenticating user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password=form.password.data)
        if user:
            add_user_to_session(user)
            return redirect(f'/users/{user.id}')
        else:
            flash("Incorrect Username or Password", 'error')
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
                flash("User created", 'success')
                return redirect(f'/users/{new_user.id}')
            except IntegrityError:
                db.session.rollback()
                flash("Username already taken", 'error')
                return redirect('/register')
            except:
                db.session.rollback()
                flash("Error creating user", 'error')
                return redirect('/register')
    return render_template('register.html', form=form)

@app.route('/users')
def redirect_to_users_all():
    return redirect('/users/all/1')

@app.route('/users/all/<int:page>')
def show_users(page):
    
    users = User.query.paginate(per_page=20, page=page)

    return render_template('users.html', users=users)

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
            if form.image.data:
                try:
                    img = Image.open(request.files[form.image.name])
                    flash("We got the image")
                    size = (300, 300)
                    img.thumbnail(size)
                    key_stub = f"profile-images/{id}/{id}_full"
                    file_key = handle_image_upload(img, key_stub)
                    user.img_url = file_key
                    db.session.commit()
                    return redirect(f'/users/{user.id}')
                except:
                    flash("Image Error", 'error')
                    return redirect(f'/users/{user.id}')
        except:
                    flash("Changes could not be saved", 'error')
                    return redirect(f'/users/{user.id}')
    return render_template('edit-user.html', user=user, form=form)

@app.route('/users/<int:id>/add_card', methods=['GET', 'POST'])
def add_new_card(id):
    form = CardForm()
    if form.validate_on_submit():
        new_card = Card.create(owner_id=id,
                        player=form.player.data,
                        year=form.year.data,
                        set_name=form.set_name.data,
                        number=form.number.data,
                        desc=form.desc.data)
        db.session.add(new_card)
        try:
            db.session.commit()
            flash("Card successfully added!", 'success')
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
                    flash("Image file is unsupported type", 'error')
            return redirect(f'/users/{id}')
        except:
            db.session.rollback()
            flash("Error adding Card", 'error')
    return render_template('add-card.html', form=form)

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    try:
        db.session.commit()
        flash("User Deleted!", 'success')
        return redirect('/logout')
    except:
        db.session.rollback()
        flash("Error deleting user", 'error')
        return redirect("/")

@app.route('/cards')
def show_cards():
    cards = Card.query.order_by(Card.year.desc()).all()
    return render_template('cards.html', cards=cards)

@app.route('/cards/<int:id>')
def show_card(id):
    card = Card.query.get_or_404(id)
    requests = [request for request in card.requests if request.accepted == None and request.valid_items]
    form = TradeRequestForm()
    print(f'\n\n{requests}\n\n')
    return render_template('card.html', card=card, requests=requests, form=form)

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
        if form.image.data:
            try:
                img = Image.open(request.files[form.image.name])
                large = (600, 600)
                img.thumbnail(large)
                key_stub = f"card_images/{card.id}_full"
                file_key = handle_image_upload(img, key_stub)
                thumb_key_stub = f"card_images/{card.id}_thumb"
                size = (150, 150)
                img.thumbnail(size)
                thumb_file_key = handle_image_upload(img, thumb_key_stub)
                card.img_url = file_key
                db.session.commit()
            except:
                flash("Image file is unsupported type", 'error')
        try:
            db.session.commit()
            flash("Changes saved", 'success')
            return redirect(f'/users/{card.user.id}')
        except:
            db.session.rollback()
            flash("error saving changes", 'error')
    return render_template('edit-card.html', form=form, card=card)

@app.route('/cards/<int:id>/request')
def request_trade(id):
    card = Card.query.get_or_404(id)
    msg = f"Request for {card.to_string()} from user {g.user.username}"
    return render_template('request.html', msg=msg)

@app.route('/cards/<int:id>/new-request', methods=['GET', 'POST'])
def create_trade_request(id):
    if g.user:
        if request.method == 'POST':
            data = request.json['request']
            new_request = TradeRequest(to_id=data['to_id'], from_id=data['from_id'])
            db.session.add(new_request)
            db.session.commit()
            for id in data['offeredCards']:
                request_card = RequestCard(request_id=new_request.id, card_id=id)
                db.session.add(request_card)
                db.session.commit()
            requested_card = RequestCard(request_id=new_request.id, card_id=data['requestedCardId'], requested=True)
            db.session.add(requested_card)
            db.session.commit()
        else:
            requested_card = Card.query.get_or_404(id)
            g_user_cards = g.user.cards
            card_json = []
            for card in g_user_cards:
                card_json.append(card.serialize())
            return render_template('new-request.html', cards=card_json, requested_card=requested_card)
    return redirect('/')


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
    if not g.user:
        return redirect('/')
    results = []
    query = Card.query
    tokens = request.args.get('tokens', None)
    if tokens:
        json_tokens = json.loads(tokens)
        for token in json_tokens:
            query = query.filter(Card.title.ilike(f'%{token}%'))
    cards = query.all()
    for card in cards:
        results.append(card.serialize())
    return jsonify(results=results)

@app.route('/api/users')
def get_users():
    if not g.user:
        return redirect('/')
    username = request.args.get('name', None)
    user_results = []
    if username:
        query_results = User.query.filter(User.username.ilike(f'%{username}%'))
        for result in query_results:
            user_results.append(result.serialize())
    else:
        all_users = User.query.all()
        for user in all_users:
            user_results.append(user.serialize())
    return jsonify(user_results)

@app.route('/users/<int:id>/requests', methods=['GET', 'POST'])
def show_requests(id):
    form = TradeRequestForm()
    requests = TradeRequest.query.filter((TradeRequest.to_id == id) | (TradeRequest.from_id == id)).order_by(TradeRequest.last_updated.desc()).all()
    if form.validate_on_submit():
        request = TradeRequest.query.get_or_404(int(form.request_id.data))
        handle_request_response(request, form)
        # if form.delete.data:
        #     db.session.delete(request)
        #     req_ID = request.id
        #     req_cards = RequestCard.query.filter_by(request_id=req_ID).delete()
        #     db.session.commit()
        #     return redirect('/')
        # elif form.decline.data:
        #     request.accepted = False
        #     request.last_updated = datetime.datetime.utcnow()
        #     db.session.commit()
        #     return redirect('/')
        # else:
        #     if request.valid_items and request.accepted == None:
        #         to_id = request.to_id
        #         from_id = request.from_id
        #         cards = request.cards
        #         for card in cards:
        #             card_requests = card.requests
        #             if card.owner_id == to_id:
        #                 card.owner_id = from_id
        #             else:
        #                 card.owner_id = to_id
        #             for request in card_requests:
        #                 request.valid_items = False
        #         request.accepted = True
        #         request.last_updated = datetime.datetime.utcnow()
        #         #### set other trade_requests with cards to valid_items = False
        #         db.session.commit()
    return render_template('requests2.html', requests=requests, form=form)

@app.route('/logout')
def logout_user():
    session.pop(USER_ID)
    flash("Goodbye!", 'success')
    return redirect('/')

def add_user_to_session(user):
    session[USER_ID] = user.id


@app.route("/api/ebay")
def ebay():
    query_string = request.args.get('item')
    return get_recent_prices(query_string)

@app.route('/ac')
def ac():
    return render_template('testAlert.html')

@app.route('/checks')
def checks():
    return render_template('checksTest.html')

@app.route('/json')
def test_json():
    card = Card.query.first()
    card_json = card.serialize()
    return render_template('test-json.html', json=card_json)


@app.route('/localtime')
def local_time():
    time = TimeTest.query.get(1)
    localtime = float(time.time.strftime("%s"))
    #converted = datetime.datetime.fromtimestamp(converted)
    #return f"{datetime.datetime.fromtimestamp(localtime)}"
    UTC_datetime = datetime.datetime.utcnow()
    UTC_datetime_timestamp = float(UTC_datetime.strftime("%s"))
    UTC_datetime_timestamp = float(UTC_datetime.strftime("%s"))
    local_datetime_converted = datetime.datetime.fromtimestamp(UTC_datetime_timestamp)
    return f"{local_datetime_converted}"

@app.route('/request_test/<int:id>')
def test_request(id):
    card = Card.query.get(id)
    request = TradeRequest(from_id=g.user.id, to_id=card.owner_id)
    db.session.add(request)
    db.session.commit()

@app.route('/test-accept', methods=['GET', 'POST'])
def test_accept():
    form = AcceptDeclineForm(hidden="CHOP")
    if form.validate_on_submit():
        print(f'\n\nGOT HERE\n\n')
        print(form.accept.data)
        print(form.decline.data)
        print(form.hidden.data)
        import pdb
        pdb.set_trace()
    return render_template('test-accept.html', form=form)

@app.route('/trade-cell')
def test_trade_cell():
    requests = RequestCard.query.filter_by(card_id=6).all()
    print(f'\n\n{requests}\n\n')
    return render_template('test-trade-cell.html')

def handle_request_response(request, form):
    if form.delete.data:
        db.session.delete(request)
        req_ID = request.id
        req_cards = RequestCard.query.filter_by(request_id=req_ID).delete()
        db.session.commit()
        return redirect('/')
    elif form.decline.data:
        request.accepted = False
        request.last_updated = datetime.datetime.utcnow()
        db.session.commit()
        return redirect('/')
    else:
        if request.valid_items and request.accepted == None:
            to_id = request.to_id
            from_id = request.from_id
            cards = request.cards
            for card in cards:
                card_requests = card.requests
                if card.owner_id == to_id:
                    card.owner_id = from_id
                else:
                    card.owner_id = to_id
                for request in card_requests:
                    request.valid_items = False
            request.accepted = True
            request.last_updated = datetime.datetime.utcnow()
            #### set other trade_requests with cards to valid_items = False
            db.session.commit()


