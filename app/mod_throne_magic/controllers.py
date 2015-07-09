#!/usr/bin/python2

import cPickle
from flask import Blueprint, render_template, session, request
from flask.ext.cache import Cache
import json
import model
import sqlite3

# User imports.
import throne


mod_throne_magic = Blueprint('throne_magic', __name__, url_prefix="/magic/tm")


@mod_throne_magic.route("/")
def index():
  session["throne"] = cPickle.dumps(throne.Throne())

  return render_template("throne_magic/index.html")


## Components #################################################################
@mod_throne_magic.route("/components/roles")
def compRoles():
  aRoles = sorted(list(k for k in cPickle.loads(session["throne"]).myD.iterkeys()))
  return render_template("throne_magic/components/roles.html", theRoles=aRoles)


@mod_throne_magic.route("/components/thrones")
def compThrones():
  aThrones = cPickle.loads(session["throne"]).myThrones
  return render_template("throne_magic/components/thrones.html", theThrones=aThrones)


@mod_throne_magic.route("/components/holdings")
def compHoldings():
  aHoldings = cPickle.loads(session["throne"]).myHoldings
  return render_template("throne_magic/components/holdings.html", theHoldings=aHoldings)


@mod_throne_magic.route("/components/seasons")
def compSeasons():
  aSeasons = cPickle.loads(session["throne"]).mySeasons
  return render_template("throne_magic/components/seasons.html", theSeasons=aSeasons)
###############################################################################


## Roles ######################################################################
@mod_throne_magic.route("/roles/primer")
def rolesPrimer():
  return render_template("throne_magic/roles/primer.html")


@mod_throne_magic.route("/roles/basic")
def rolesBasic():
  return render_template("throne_magic/roles/basic.html")


@mod_throne_magic.route("/roles/draft")
def rolesDraft():
  aRoles = sorted(list(k for k in cPickle.loads(session["throne"]).myD.iterkeys()))
  return render_template("throne_magic/roles/draft.html", theRoles=aRoles)


@mod_throne_magic.route("/roles/random")
def rolesRandom():
  return render_template("throne_magic/roles/random.html")
###############################################################################


## Rules ######################################################################
@mod_throne_magic.route("/rules")
def rules():
  return render_template("throne_magic/rules.html")


@mod_throne_magic.route("/rules/advanced")
def advancedRules():
  return "woo"
###############################################################################


## API ########################################################################
@mod_throne_magic.route("/api/select", methods=["POST"])
def select():
  session["throne"] = cPickle.dumps(throne.Throne())

  if request.method == "POST":
    aThrone = cPickle.loads(session["throne"])
    aThrone.selectRole(request.form["aRole"])

    aRet = json.dumps( #aThrone.myAllowed)
      {
        "selected": json.dumps(aThrone.mySel),
        # "allowed": json.dumps(aThrone.myAllowed)
        "mustElim": json.dumps(aThrone.myMustEliminate),
        "elimBy": json.dumps(aThrone.myEliminatedBy)
      }
    )

    # Load the pickle back into the session.
    session["throne"] = cPickle.dumps(aThrone)

    # Return the json.
    return aRet


@mod_throne_magic.route("/api/random")
def random():
  session["throne"] = cPickle.dumps(throne.Throne())

  aThrone = cPickle.loads(session["throne"])
  aRet = json.dumps(aThrone.getRandom(int(request.args["aNumber"])))

  # Load the pickle back into the session.
  session["throne"] = cPickle.dumps(aThrone)

  return aRet
###############################################################################

