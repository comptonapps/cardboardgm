from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FileField, SubmitField, HiddenField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Optional
from wtforms_validators import AlphaNumeric
from constants import EARLIEST_YEAR, CURRENT_YEAR


class UsernameForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), AlphaNumeric(message="Username must only contain letters and numbers"), Length(min=3, max=20, message="Username must be between 3 and 20 characters")])

class LoginForm(UsernameForm):
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=20, message="Password must be between 6 and 20 characters")])

class RegisterForm(LoginForm):

    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class EditUserForm(RegisterForm):
    image = FileField("Avatar Img", validators=[Optional()], id="foo")

class PlayerForm(FlaskForm):
    player = StringField("Player", validators=[InputRequired()])
    
class CardForm(PlayerForm):
    year = SelectField("Year", choices=[(year, year) for year in reversed(range(EARLIEST_YEAR, CURRENT_YEAR + 1))], validators=[Optional()])
    set_name = StringField("Set", validators=[InputRequired()])
    number = StringField("Number", validators=[Optional()])
    desc = StringField("Description", validators=[Length(max=50, message="Limit description to 50 characters")])
    image = FileField("Card Image", validators=[Optional()])

class TradeRequestForm(FlaskForm):
    accept = SubmitField('Accept')
    decline = SubmitField('Decline')
    delete = SubmitField('Remove Request')
    request_id = HiddenField(IntegerField())

class HiddenRequestForm(FlaskForm):
    req_data = HiddenField()