#!/usr/bin/python2

from flask import Flask, render_template, url_for, redirect, request, flash, \
                  session, Blueprint, jsonify
from flask.ext.mail import Mail, Message

import hashlib
import json
from app.mod_resume.models import *
import os
import re
import shutil
import subprocess
import time


mod_resume = Blueprint('resume', __name__, url_prefix="/resume")


def getData():
  aCore = Core.query.first()
  aEdus = Education.query.order_by(Education.start.desc()).all()
  aJobs = Job.query.order_by(Job.start.desc()).all()
  aDuties = {}
  for aJob in aJobs:
    aDuties[aJob.id] = JobDuty.query.filter_by(companyid=aJob.id).all()
  aSkillCats = SkillCategory.query.all()
  aSkills = {}
  for aSkillCat in aSkillCats:
    aSkills[aSkillCat.id] = Skill.query.filter_by(categoryid=aSkillCat.id).all()
  aAwards = Award.query.all()

  return {
    "core": aCore,
    "edus": aEdus,
    "jobs": aJobs,
    "duties": aDuties,
    "skillCats": aSkillCats,
    "skills": aSkills,
    "awards": aAwards
  }


@mod_resume.route('/')
def index():
  aData = getData()

  return render_template(
    "resume/resume.html",
    theCore=aData["core"],
    theEdus=aData["edus"],
    theJobs=aData["jobs"],
    theDuties=aData["duties"],
    theSkillCats=aData["skillCats"],
    theSkills=aData["skills"],
    theAwards=aData["awards"]
  )


def getTemplate(theName, theData):
  """Gets the template and inserts the data, returning a string."""
  # Get the template.
  aTemplate = myTemplates[theName]
  aRet = ""

  if isinstance(theData, list):
    # If the string is an array, start looping.
    for i in theData:
      aRet += aTemplate.format(**i)
  else:
    # Otherwise just format it.
    aRet = aTemplate.format(**theData)

  # Return the formatted template.
  return aRet


@mod_resume.route("/gen")
def generate():
  # Get the data.
  aData = getData()

  # Insert it into the templates, saving each one.
  aFile = getTemplate("file", None)
  for k, v in aData:
    aFile.format(k, getTemplate(k, v))

  # Write the file out to the fs.

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


