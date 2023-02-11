from wtforms import Form, StringField, SubmitField, validators, PasswordField, EmailField
from flask_wtf.file import FileField


class SettingsForm(Form):
    username = StringField('Username', [validators.InputRequired(), validators.Length(min=4, max=25)])
    email = EmailField('Email Address',
                       [validators.InputRequired(), validators.Email(), validators.Length(min=6, max=35)])
    full_name = StringField('Full name', [validators.InputRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.InputRequired()])
    bio = StringField('Bio')
    profile_pic = FileField('Profile Pic')
    submit = SubmitField("Save")
