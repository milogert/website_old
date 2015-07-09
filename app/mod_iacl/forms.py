# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, SelectMultipleField, RadioField, BooleanField

# Import Form validators
from wtforms.validators import Required, EqualTo

# Config for forms.
import app.mod_iacl.config as config


# Define the login form (WTForms)

class CampaignSetup(Form):
  name = TextField("Name")

  heroes = SelectMultipleField(
    "Heroes",
    choices=[(key, key) for key in config.myHeroes.keys()]
  )

  agendas = SelectMultipleField(
    "Agendas",
    choices=[(key, key) for key in config.myAgendas.keys()]
  )

  # Get only the hero, rebel, and random missions.
  c = []
  for key, value in config.myMissions.items():
    if value["type"] in ("Rebel", "Random"):
      c.append((key, key))

  missions = SelectMultipleField(
    "Missions",
    choices=c
  )

  imperialClasses = RadioField(
    "Imperial Classes",
    choices=[(key, key) for key in config.myImperialClasses.keys()]
  )

