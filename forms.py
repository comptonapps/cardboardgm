from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FileField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Optional
from wtforms_validators import AlphaNumeric
from constants import EARLIEST_YEAR, CURRENT_YEAR



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), AlphaNumeric(message="Username must only contain letters and numbers"), Length(min=3, max=20, message="Username must be between 3 and 20 characters")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=20, message="Password must be between 6 and 20 characters")])

class RegisterForm(LoginForm):

    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class CardForm(FlaskForm):

    player = StringField("Player", validators=[InputRequired()])
    year = SelectField("Year", choices=[(year, year) for year in reversed(range(EARLIEST_YEAR, CURRENT_YEAR + 1))], validators=[Optional()])
    set_name = StringField("Set", validators=[InputRequired()])
    number = StringField("Number", validators=[Optional()])
    description = StringField("Description", validators=[Length(max=50)])
    image = FileField("Card Image", validators=[Optional()])