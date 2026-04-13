from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    poster = FileField('Movie Poster', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])