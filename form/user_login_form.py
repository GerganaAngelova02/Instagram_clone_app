from wtforms import Form, SubmitField, validators, PasswordField, EmailField


class LoginForm(Form):
    email = EmailField('Email Address', [validators.InputRequired(), validators.Email(), validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Login')
