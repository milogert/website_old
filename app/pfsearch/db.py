
from flask.ext.mongoengine import MongoEngine
from mongoengine import *

class Spell(Document):
  # Classes.
  alchemist = StringField()
  antipaladin = StringField()
  bard = StringField()
  bloodline = StringField()
  bloodrager = IntField()
  cleric = StringField()
  druid = StringField()
  inquisitor = StringField()
  magus = IntField()
  oracle = StringField()
  paladin = StringField()
  ranger = StringField()
  summoner = StringField()
  sor = IntField()
  wiz = IntField()
  witch = StringField()

  # Domain.
  air = IntField()
  chaotic = IntField()
  cold = IntField()
  darkness = IntField()
  death = IntField()
  earth = IntField()
  domain = StringField()
  evil = IntField()
  fear = IntField()
  fire = IntField()
  focus = IntField()
  force = IntField()
  emotion = IntField()
  electricity = IntField()
  good = IntField()
  lawful = IntField()
  light = IntField()
  shadow = IntField()
  water = IntField()


  SLA_Level = IntField()
  acid = IntField()
  adept = StringField()
  area = StringField()
  augmented = StringField()
  casting_time = StringField()
  components = StringField()
  costly_components = IntField()
  curse = IntField()
  deity = StringField()
  description = StringField()
  description_formated = StringField()
  descriptor = StringField()
  disease = IntField()
  dismissible = IntField()
  divine_focus = IntField()
  duration = StringField()
  effect = StringField()
  full_text = StringField()
  id = IntField()
  language_dependent = IntField()
  linktext = StringField()
  material = IntField()
  material_costs = StringField()
  mind_affecting = IntField()
  mythic = IntField()
  mythic_text = StringField()
  name = StringField()
  pain = IntField()
  patron = StringField()
  poison = IntField()
  range = StringField()
  saving_throw = StringField()
  school = StringField()
  shaman = StringField()
  shapeable = IntField()
  short_description = StringField()
  somatic = IntField()
  sonic = IntField()
  source = StringField()
  spell_level = StringField()
  spell_resistence = StringField()
  subschool = StringField()
  targets = StringField()
  verbal = IntField()
