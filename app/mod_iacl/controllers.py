# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, abort

import json
import random, string

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db#, redirect_back, get_redirect_target

# Import module models (i.e. User)
from app.mod_iacl.models import AgendaSet, AgendaSub, Campaign, Empire, EmpireSkill, Hero, HeroGear, HeroSkill, Mission, Reward

# Import module forms
from app.mod_iacl.forms import CampaignSetup

import app.mod_iacl.config as config

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_iacl = Blueprint('iacl', __name__, url_prefix='/games/iacl')


# Set the route and accepted methods
@mod_iacl.route('/')
def index():
  # Stuff for heroes.
  aSetup = CampaignSetup(request.form)

  return render_template("iacl/new.html", theSetup=aSetup)


@mod_iacl.route('/new', methods=["POST"])
def newGame():
  if request.method == "POST":
    # Create the form.
    aSubmit = CampaignSetup(request.form)

    # Generate a hash code.
    aCode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    # Put the data into the database.
    db.session.add(Campaign(code=aCode, name=aSubmit.name.data))

    # Commit once to get the Campaign in there.
    db.session.commit()

    # Hero data.
    for aHero in aSubmit.heroes.data:
      # Add the actual hero.
      db.session.add(Hero(code=aCode, name=aHero))

      # Add the hero's mission.
      db.session.add(Mission(code=aCode, name=config.myHeroes[aHero]["mission"]))

    # Commit Rebel data.
    db.session.commit()

    # Hero gear.
    for aHero in aSubmit.heroes.data:
      db.session.add(HeroGear(code=aCode, name=config.myHeroes[aHero]["startingWeapon"]))

    # Commit Rebel gear.
    db.session.commit()

    # Agenda set data.
    aAgendaList = []
    aSubList = []
    for aAgendaSet in aSubmit.agendas.data:
      aAgendaList.append(AgendaSet(code=aCode, setname=aAgendaSet))
      for aSubAgenda in config.myAgendas[aAgendaSet]:
        aSubList.append(AgendaSub(code=aCode, setname=aAgendaSet, name=aSubAgenda["name"]))

    # Agenda set data.
    for a in aAgendaList:
      db.session.add(a)
    db.session.commit()

    # Agenda subset data.
    for a in aSubList:
      db.session.add(a)
    db.session.commit()

    # Mission data.
    for aMission in aSubmit.missions.data:
      db.session.add(Mission(code=aCode, name=aMission))

    # Empire data.
    aClass = aSubmit.imperialClasses.data
    db.session.add(Empire(code=aCode, cls=aClass))
    db.session.commit()

    db.session.add(EmpireSkill(
      code=aCode,
      cls=aClass,
      name=config.myImperialClasses[aClass]["startingSkill"]
    ))
    db.session.commit()

    # Redirect to the view.
    return redirect(url_for(".view", theId=aCode))
  else:
    abort(405)


@mod_iacl.route('/view/<theId>')
def view(theId):
  # Get the data from the database with theId.
  aCampaign = Campaign.query.filter_by(code=theId).first()
  aHeroes = Hero.query.filter_by(code=theId).all()
  aGear = HeroGear.query.filter_by(code=theId).all()

  # Get the skills and place them on the appropriate heros.
  aSkills = {}
  for aHero in aHeroes:
    aSkills[aHero.name] = {"purchased": [], "available": []}
  for aHero, aSkillSet in aSkills.items():
    aSkills[aHero]["purchased"] = HeroSkill.query.filter_by(code=theId, name=aHero).all()
  for aHero, aSkillSet in aSkills.items():
    aPotAvail = [aSkill for aSkill in config.myHeroes[aHero]["skills"]]
    aPurchased = [aSkill.title for aSkill in aSkillSet["purchased"]]
    aSkills[aHero]["available"] = [x for x in aPotAvail if x["name"] not in aPurchased]

  # Get the Empire information.
  aEmpire = Empire.query.filter_by(code=theId).first()
  aESkills = {
    "purchased": EmpireSkill.query.filter_by(code=theId).all(),
    "available": []
  }
  aPotAvail = [aSkill for aSkill in config.myImperialClasses[aEmpire.cls]["skills"]]
  aPurchased = [aSkill.name for aSkill in aESkills["purchased"]]
  aESkills["available"] = [x for x in aPotAvail if x["name"] not in aPurchased]

  # Get the agendas.
  aSets = [k.setname for k in AgendaSet.query.filter_by(code=theId).all()]
  aAgendas = {k: v for k, v in config.myAgendas.items() if k in aSets}

  return render_template(
    "iacl/view.html",
    theCampaign=aCampaign,
    theHeroes=aHeroes,
    theGear=aGear,
    theSkills=aSkills,
    theEmpire=aEmpire,
    theESkills=aESkills,
    theAgendas=aAgendas
  )


@mod_iacl.route('/buy')
def buy():
  return jsonify(request.args)


@mod_iacl.route('/sell')
def sell():
  return jsonify(request.args)


@mod_iacl.route('/activate')
def activate():
  return jsonify(request.args)


@mod_iacl.route('/discard')
def discard():
  return jsonify(request.args)


# @mod_boardgames.route('/setNext', methods=["POST"])
# def setNext():
#   if request.method == "POST":
#     aJson = request.get_json()
#     print aJson

#     # Get the row from the database.
#     aUpdate = Boardgame.query.filter_by(id=aJson["id"]).first()

#     print aUpdate

#     # Change the values.
#     aUpdate.playNext = aJson["playNext"]
#     aUpdate.playsLeft = aJson["playsLeft"]

#     print aUpdate

#     # Commit the change.
#     db.session.commit()

#     return abort(404)
#   else:
#     abort(405)
