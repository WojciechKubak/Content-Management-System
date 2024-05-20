from flask_wtf import FlaskForm, validators
from wtforms import StringField, PasswordField, IntegerField


class CommentForm(FlaskForm):
    """
    CommentForm Class

    This class defines a WTForms-based form for validating comment input.

    Attributes:
        content (StringField): A StringField for the comment content with data validation.
        article_id (IntegerField): An IntegerField for the article ID with data validation.
        user_id (IntegerField): An IntegerField for the user ID with data validation.
    """
    content = StringField('Content', validators=[
        validators.DataRequired(),
        validators.Length(max=2000, message='Content must be no more than 2000 characters')
    ])

    article_id = IntegerField('Article ID', validators=[
        validators.DataRequired(),
        validators.NumberRange(min=1, message='Article ID must be a positive integer')
    ])

    user_id = IntegerField('User ID', validators=[
        validators.DataRequired(),
        validators.NumberRange(min=1, message='User ID must be a positive integer')
    ])


class UserForm(FlaskForm):
    """
    UserForm Class

    A FlaskForm subclass for user registration and update forms.

    Attributes:
        username (StringField): Form field for the user's username. 
            It is required and must be between 4 and 20 characters.
        email (StringField): Form field for the user's email address. 
            It is required, must be between 6 and 255 characters, and must be a valid email address.
        password (PasswordField): Form field for the user's password. 
            It is required and must be at least 6 characters long.
    """
    username = StringField('Username', [
        validators.DataRequired(message='Username is required.'),
        validators.Length(min=4, max=20, message='Username must be between 4 and 20 characters.')
    ])
    email = StringField('Email Address', [
        validators.DataRequired(message='Email is required.'),
        validators.Length(min=6, max=255, message='Email must be between 6 and 255 characters.'),
        validators.Email(message='Invalid email address.')
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message='Password is required.'),
        validators.Length(min=6, max=255, message='Password must be at least 6 characters long.')
    ])


class LoginForm(FlaskForm):
    """
    LoginForm Class

    This class defines a WTForms-based form for validating user login input.

    Attributes:
        username (StringField): A StringField for the username with data validation.
        password (PasswordField): A PasswordField for the password with data validation.
    """
    username = StringField('Username', [
        validators.DataRequired(message='Username is required.'),
        validators.Length(min=4, max=20, message='Username must be between 4 and 20 characters.')
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message='Password is required.'),
        validators.Length(min=6, max=20, message='Password must be at least 6 characters long.'),
    ])


class RegistrationForm(FlaskForm):
    """
    RegistrationForm Class

    This class defines a WTForms-based form for validating user registration input.

    Attributes:
        username (StringField): A StringField for the username with data validation.
        email (StringField): A StringField for the email address with data validation.
        password (PasswordField): A PasswordField for the password with data validation.
    """
    username = StringField('Username', [
        validators.DataRequired(message='Username is required.'),
        validators.Length(min=4, max=20, message='Username must be between 4 and 20 characters.')
    ])
    email = StringField('Email Address', [
        validators.DataRequired(message='Email is required.'),
        validators.Length(min=6, max=35, message='Email must be between 6 and 35 characters.'),
        validators.Email(message='Invalid email address.')
    ])
    password = PasswordField('New Password', [
        validators.DataRequired(message='Password is required.'),
        validators.Length(min=6, max=20, message='Password must be at least 6 characters long.'),
    ])
