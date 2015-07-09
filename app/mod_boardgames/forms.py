# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, SelectField, DecimalField, IntegerField, BooleanField

# Import Form validators
from wtforms.validators import Required, EqualTo


# Define the login form (WTForms)

class NewGame(Form):
    name = TextField(
      'Name'
    )
    acquired = SelectField(
      "Acquired",
      choices=[
        ("Amazon", "Amazon"),
        ("FLGS", "FLGS"),
        ("Gift", "Gift"),
        ("Kickstarter", "Kickstarter"),
        ("Massdrop", "Massdrop")
      ]
    )
    cost = DecimalField(
      'Cost',
      places=2
    )
    plays = IntegerField(
      'Plays'
    )
    averageTime = DecimalField(
      'Average Time',
      places=2
    )
    playNext = BooleanField(
      'Play Next?'
    )
    hasArrived = BooleanField(
      'Play Next?'
    )
    status = SelectField(
      "Status",
      choices=[
        ("", ""),
        ("Default", "Default"),
        ("Play Next", "Play Next"),
        ("Has Not Arrived", "Has Not Arrived")
      ]
    )


class ExistingGame(Form):
    status = SelectField(
      "Status",
      choices=[
        ("", ""),
        ("Default", "Default"),
        ("Play Next", "Play Next"),
        ("Has Not Arrived", "Has Not Arrived")
      ]
    )
