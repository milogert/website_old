#!/usr/bin/python2

from flask import Flask, render_template, url_for, redirect, request, flash, \
                  session, Blueprint, jsonify
from flask.ext.mail import Mail, Message

import hashlib
import json
from app.mod_personal.models import getGames
import os
import re
import shutil
import subprocess
import time


mod_personal = Blueprint('personal', __name__, url_prefix="")


@mod_personal.route('/')
def index():
  return render_template("personal/index.html")


@mod_personal.route("/resume/gen")
def resumePdf():
  # Copy the file to the backup.
  aGlob = r"app/static/resume/resume_*.pdf"
  aDest = "app/static/resume/bak"
  import glob

  # Move any file found.
  for aFile in glob.glob(aGlob):
    shutil.move(aFile, aDest)

  # Clean up the backup directory.
  aGlob = r"app/static/resume/bak/resume_*.pdf"
  aFileList = glob.glob(aGlob)
  aFileList.sort()
  aListLen = len(aFileList) - 10
  for i in xrange(0, aListLen):
    os.unlink(aFileList[i])

  # Generate a new pdf.
  aRet = subprocess.call([
      "pdflatex",
      "-output-directory=app/static/resume",
      "app/static/resume/resume.tex"
  ])

  if aRet == 0:
    import datetime
    d = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    shutil.move(
        "app/static/resume/resume.pdf",
        "app/static/resume/resume_" + d + ".pdf"
    )
    return redirect(url_for('static', filename='resume/resume_' + d + '.pdf'))
  else:
    return "didn't work" #redirect(url_for('static', filename='resume/bak/resume.pdf', nocache=str(time.time())))


@mod_personal.route("/contact", methods=["GET", "POST"])
def contact():
  if True:
    return "Currently broken"

  if request.method == "POST":
    aName = request.form["name"]
    aEmail = request.form["email"]
    aMessage = request.form["message"]

    # Check if the email provided is a valid one.
    if re.match(r"[^@]+@[^@]+\.[^@]+", aEmail):
      aSubject = "Inquiry from {0}"
      aBody = "From {0} ({1})\n\n{2}"

      # Create the email.
      aMsg = Message(
        aSubject.format(aName),
        sender=(aName, aEmail),
        recipients=["milo@milogert.com"]
      )

      # Prepare the body.
      aMsg.body = aBody.format(aName, aEmail, aMessage)

      # Send the email.
      myMail.send(aMsg)

      flash("Message sent!")
      return render_template("personal/contact.html")

  return render_template("personal/contact.html")


@mod_personal.route("/games")
def games():
  if True:
    return "Currently broken."

  if "username" not in session or session["username"] != "milo":
    return redirect(url_for("personal.index"))

  aGames = getGames()
  return render_template("personal/games.html", theGames=aGames)

