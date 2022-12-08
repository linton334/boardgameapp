from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import EmailField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms.validators import DataRequired



class RegisterForm(FlaskForm):
    username = StringField('Enter Username', validators=[DataRequired()])
    email = EmailField('Enter Email', validators=[DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = EmailField('Enter Email', validators=[DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me?')

class ChangePassForm(FlaskForm):
    oldpassword = PasswordField('Enter Current Password', validators=[DataRequired()])
    password = PasswordField('Enter New Password', validators=[DataRequired()])