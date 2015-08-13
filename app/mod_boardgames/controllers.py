# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, abort

import json
import urllib
from xml.dom import minidom
from collections import Counter

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db#, redirect_back, get_redirect_target

# Import module models (i.e. User)
from app.mod_boardgames.models import Boardgame

# Import module forms
from app.mod_boardgames.forms import NewGame, ExistingGame

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_boardgames = Blueprint('boardgames', __name__, url_prefix='/games/bg')

# Set a pre request for this blueprint.
@mod_boardgames.before_request
def requireAuth():
  if ("username" not in session or session["username"] != "milo") and request.endpoint != "boardgames.index":
    return redirect(url_for("personal.index"))


# Set the route and accepted methods
@mod_boardgames.route('/')
def index():
  # If sign in form is submitted
  aNewGameForm = NewGame(request.form)
  aExistingGameForm = ExistingGame(request.form)

  aBGs = Boardgame.query.order_by(
    Boardgame.status.asc(),
    Boardgame.name.asc()
  ).all()
  aSum = 0
  aCount = 0

  for aBG in aBGs:
    if aBG.plays * aBG.averageTime > 0:
      aSum += aBG.cost / (aBG.plays * aBG.averageTime)
      aCount += 1

  # Get the average number.
  aAvg = aSum / aCount

  return render_template(
    "boardgames/boardgames.html",
    theBoardgames=aBGs,
    theAvg=aAvg,
    theNewGameForm=aNewGameForm,
    theExistingGameForm=aExistingGameForm
  )


@mod_boardgames.route('/newGame')
def newGame():
  aGame = request.args

  # Create a new boardgame object.
  aNewGame = Boardgame(
    name=aGame["name"],
    acquired=aGame["acquired"],
    cost=int(aGame["cost"]),
    plays=int(aGame["plays"]),
    averageTime=float(aGame["averageTime"]),
    playsLeft=3 if aGame["status"] == "Play Next" else 0,
    status=aGame["status"]
  )

  print aNewGame

  db.session.add(aNewGame)
  db.session.commit()

  return json.dumps({"success": True}, 200, {"ContentType": "application/json"})


@mod_boardgames.route('/addPlay')
def addPlay():
  aJson = request.args

  # Get the row from the database.
  aUpdate = Boardgame.query.filter_by(id=int(aJson["id"])).first()

  # Change the values.
  aUpdate.plays = int(aJson["plays"])
  aUpdate.playsLeft = int(aJson["playsLeft"])
  aUpdate.status = aJson["status"]

  # Commit the change.
  db.session.commit()

  return json.dumps({"success": True}, 200, {"ContentType": "application/json"})


@mod_boardgames.route('/updateStatus')
def updateStatus():
  aJson = request.args

  # Get the row from the database.
  aUpdate = Boardgame.query.filter_by(id=int(aJson["id"])).first()

  # Change the values.
  aUpdate.playsLeft = int(aJson["playsLeft"])
  aUpdate.status = aJson["status"]

  # Commit the change.
  db.session.commit()

  return json.dumps({"success": True}, 200, {"ContentType": "application/json"})


@mod_boardgames.route('/bgg/<theUsername>')
def bgg(theUsername):
  # Get the xml for a particular user.


  # Parse the xml for plays.
  aDom = minidom.parse(urllib.urlopen("http://boardgamegeek.com/xmlapi2/plays?username={}".format(theUsername)))

  # Create a dictionary for us to use.
  aPlays = Counter(aNode.getAttribute("name") for aNode in aDom.getElementsByTagName("item"))

  print aPlays
  # Use a different api to get price of the game.
  # TODO: Wait on this for later. Lets just get games up for now.

  # Send that junk to the template.
  return render_template("empty.html", theStuff=dict(aPlays))

