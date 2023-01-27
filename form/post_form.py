from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, validators


class PostForm(FlaskForm):
    content = FileField('Photo')
    caption = StringField('Caption')
    submit = SubmitField("Upload")
