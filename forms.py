from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from models import User

class UserAddForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    image_url = StringField(_l('Image URL'))
    first_name = StringField(_l('First Name'), validators=[DataRequired()])
    last_name = StringField(_l('Last Name'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))
        

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class UserEditForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()]) 
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    image_url = StringField(_l('Image URL'))
    header_image_url = StringField(_l('Header Image URL'))
    bio = StringField(_l('Bio'))
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password_confirm = PasswordField(_l('Confirm Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different email address.'))
            

