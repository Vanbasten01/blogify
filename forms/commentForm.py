from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import SubmitField, TextAreaField

class CommentForm(FlaskForm):
    comment = TextAreaField('Write Your Comment...', validators=[DataRequired(), Length(max=1000)])

    submit = SubmitField('Post')