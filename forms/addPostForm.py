from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class AddPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    image = FileField('image')
    category = SelectField('Categories', choices=[('Technology', 'Technology'), ('Science', 'Science'), ('Travel', 'Travel'), ('Health', 'Health'), ('Food', 'Food'), ('Others', 'Others')], validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    #content = TexAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish')