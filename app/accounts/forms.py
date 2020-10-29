from app.models import UserProfile
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")

    def check_username(self, username):
        user = UserProfile.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('User does not exist.')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    # date_of_birth = DateField('Date of Birth')
    submit = SubmitField('Register!')

    def check_email(self, field):
        # Here we can reject unwanted emails also
        if UserProfile.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been already registered!')

    def check_username(self, field):
        if UserProfile.query.filter_by(username=field.data).first():
            raise ValidationError('Username has already been taken!')


class SendResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Email')

    def check_email(self, email):
        user = UserProfile.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email does not exist.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')