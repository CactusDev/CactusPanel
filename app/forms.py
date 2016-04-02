from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
