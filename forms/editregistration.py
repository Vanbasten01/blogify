
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, Optional

class RegistrationFormU(FlaskForm):
    email = StringField('', validators=[
        DataRequired(),
        Regexp(r'^[\w\.-]+@[\w\.-]+\.\w+$', message='Invalid email address')
    ])
    first_name = StringField('', validators=[DataRequired()])
    last_name = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[
        Optional(),
        Length(min=8, message='Password must be at least 8 characters long'),
        EqualTo('confirm_password', message='Passwords must match'),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
               message='Password must contain uppercase, lowercase, number, and special character.')
    ])
    #confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    confirm_password = PasswordField('', validators=[
    Optional(),
    EqualTo('password', message='Passwords must match')
])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Upadate')