from flask import Flask, render_template, request, g, session, redirect, flash
from secrets import FLASK_SECRET_KEY
from models import db, connect_db, User, Card
from forms import LoginForm, RegisterForm, CardForm
from sqlalchemy.exc import IntegrityError

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
            session[USER_ID] = user.id
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
                db.session.rollback
                flash("Error creating user")
                return redirect('/register')
    return render_template('register.html', form=form)

@app.route('/users/<int:id>')
def show_user(id):
    user = User.query.get_or_404(id)
    return user.username

@app.route('/logout')
def logout_user():
    session.pop(USER_ID)
    flash("Goodbye!")
    return redirect('/')