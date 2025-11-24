from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileAllowed
from models import User

class SignUpForm(FlaskForm):
    """Form for user registration"""
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, max=80)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Create Account')
    
    def validate_email(self, email):
        """Check if email is already registered"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Login')


class CreateBlogForm(FlaskForm):
    """Form for creating a new blog post"""
    title = StringField('Blog Title', validators=[
        DataRequired(),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    excerpt = StringField('Excerpt (Short preview)', validators=[
        Length(min=0, max=500, message='Excerpt must be 500 characters or less')
    ])
    content = TextAreaField('Blog Content', validators=[
        DataRequired(),
        Length(min=10, message='Content must be at least 10 characters')
    ])
    featured_image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only! (JPG, PNG, GIF)')
    ])
    is_published = BooleanField('Publish Immediately')
    submit = SubmitField('Create Blog Post')


class EditBlogForm(FlaskForm):
    """Form for editing an existing blog post"""
    title = StringField('Blog Title', validators=[
        DataRequired(),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    excerpt = StringField('Excerpt (Short preview)', validators=[
        Length(min=0, max=500, message='Excerpt must be 500 characters or less')
    ])
    content = TextAreaField('Blog Content', validators=[
        DataRequired(),
        Length(min=10, message='Content must be at least 10 characters')
    ])
    featured_image = FileField('Featured Image (leave blank to keep current)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only! (JPG, PNG, GIF)')
    ])
    is_published = BooleanField('Publish')
    submit = SubmitField('Update Blog Post')
