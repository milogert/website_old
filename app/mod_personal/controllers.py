#!/usr/bin/python2

from flask import Flask, render_template, url_for, redirect, request, \
                  flash, session, Blueprint, jsonify
from flask.ext.mail import Mail, Message

import hashlib
import json
from app import mailer
from app.mod_personal.models import Game
from app.mod_personal.forms import Contact
import os
import re
import shutil
import subprocess
import time


mod_personal = Blueprint('personal', __name__, url_prefix="")


@mod_personal.route('/')
def index():
  return render_template("personal/index.html")


@mod_personal.route("/contact/", methods=["GET", "POST"])
def contact():
  aForm = Contact()

  if aForm.validate_on_submit():
    # Check if the email provided is a valid one.
    aSubject = "Inquiry from {0}"
    aBody = "From {0} ({1})\n\n{2}"

    # Create the email.
    aMsg = Message(
      aSubject.format(aForm.name.data),
      sender=(aForm.name.data, aForm.email.data),
      recipients=["milo@milogert.com"]
    )

    # Prepare the body.
    aMsg.body = aBody.format(aForm.name.data, aForm.email.data, aForm.message.data)

    # Send the email.
    mailer.send(aMsg)

    flash("Message sent!", "success")

    return redirect(url_for("personal.contact"))

  return render_template("personal/contact.html", theForm=aForm)


@mod_personal.route("/games")
def games():
  if "username" not in session or session["username"] != "milo":
    return redirect(url_for("personal.index"))

  aGames = Game.query.all()
  return render_template("personal/games.html", theGames=aGames)

