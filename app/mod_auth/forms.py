# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField

class LoginForm(Form):
    username = TextField(
      'Username',
      [
        Required(message='Forgot your username?')
      ]
    )
    password = PasswordField(
      'Password',
      [
        Required(message='Must provide a password.')
      ]
    )

