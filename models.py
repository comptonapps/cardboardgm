from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from constants import AWS_URL

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    img_url = db.Column(db.Text)

    cards = db.relationship("Card", backref="user", order_by="Card.year.desc()", cascade='all, delete-orphan')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        hashed = bcrypt.generate_password_hash(password)
        pwd_utf8 = hashed.decode("utf8")

        return cls(username=username,
                   password=pwd_utf8,
                   email=email,
                   first_name=first_name,
                   last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class CardMaster(db.Model):

    __tablename__ = "card_masters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player = db.Column(db.String(50), nullable=False)
    set_name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(20), nullable=False)

class Card(db.Model):

    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #master = db.Column(db.Integer, db.ForeignKey("card_masters.id"))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    player = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    set_name = db.Column(db.Text, nullable=False)
    number = db.Column(db.Text)
    desc = db.Column(db.Text)
    img_url = db.Column(db.Text, default=None)

    def serialize(self):
        return {'player'      : self.player,
                'year'        : self.year,
                'set_name'    : self.set_name,
                'number'      : self.number,
                'description' : self.desc,
                'img_url'     : self.img_url}

    def to_string(self):
        return f"{self.year} {self.set_name} #{self.number} {self.player} {self.desc}"

    def full_img_url(self):
        return f"{AWS_URL}{self.img_url}"

    def thumb_url(self):
        if self.img_url:
            thumbnail_url = self.img_url.replace("_full", "_thumb")
            return f"{AWS_URL}{thumbnail_url}"
        else:
            return None

