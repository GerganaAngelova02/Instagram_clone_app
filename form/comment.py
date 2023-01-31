from flask_wtf import Form
from wtforms import StringField, SubmitField, validators


class CommentForm(Form):
    comment = StringField('Comment', [validators.InputRequired()])
    submit = SubmitField("Post")
