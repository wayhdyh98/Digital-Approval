from flask_wtf import Form
from wtforms import StringField, PasswordField
import wtforms.validators as validators


class SignUp(Form):
    first_name = StringField(
        'Name', validators=[validators.input_required(), validators.length(min=2)])
    last_name = StringField('Surname', validators=[
                            validators.input_required(), validators.length(min=2)])
    phone = StringField('Phone number', validators=[
                        validators.input_required(), validators.length(min=6)])
    email = StringField('Email address', validators=[
                        validators.input_required(), validators.email()])
    password = PasswordField('Password', validators=[
        validators.input_required(), validators.length(min=6), validators.equal_to('confirm', 'Passwords must match.')])
    confirm = PasswordField('Confirm password')


class SignIn(Form):
    userid = StringField('User Id', validators=[
        validators.input_required()])
    password = PasswordField('Password', validators=[
        validators.input_required(), validators.length(min=6)])
