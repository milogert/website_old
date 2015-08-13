# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, TextAreaField

# Import Form validators
from wtforms.validators import Required, EqualTo, Email


# Define the login form (WTForms)

class Contact(Form):
    name = TextField('Name')
    email = TextField('Email', [Email(message="Please enter a valid email.")])
    message = TextAreaField('Message')


