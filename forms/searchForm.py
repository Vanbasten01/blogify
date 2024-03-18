from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField
from wtforms.validators import DataRequired


class Searchform(FlaskForm):
    keyword = SearchField('Keyword', validators=[DataRequired()] )
    submit = SubmitField('Search')