from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import EmailField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired(), Length(max = 100)])
    email = EmailField('Enter Email', validators=[DataRequired(), Length(max = 150)])
    password = PasswordField('Enter Password', validators=[DataRequired(), Length(max = 100)])

class LoginForm(FlaskForm):
    email = EmailField('Enter Email', validators=[DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me?')

class ChangePassForm(FlaskForm):
    oldpassword = PasswordField('Enter Current Password', validators=[DataRequired()])
    password = PasswordField('Enter New Password', validators=[DataRequired(), Length(max = 100)])