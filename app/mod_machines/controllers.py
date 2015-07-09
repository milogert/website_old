#!/usr/bin/python2

from flask import Flask, render_template, url_for, redirect, request, flash, \
                  session, Blueprint, jsonify
from flask.ext.mail import Mail, Message

import hashlib
import json
import os
import re
import shutil
import subprocess
import time

# Import models.
from app.mod_machines.models import Spec, OS, Drive, Display

# Create the blueprint.
mod_machines = Blueprint('machines', __name__, url_prefix="/machines")


@mod_machines.route("/")
def index():
  # Create a dictionary.
  aDict = {}

  # Get the machines.
  for aSpec in Spec.query.all():
    aName = aSpec.name
    aDict[aName] = {}
    aDict[aName]["Specs"] = [aSpec]
    aDict[aName]["Displays"] = Display.query.filter_by(name=aName).all()
    aDict[aName]["Drives"] = Drive.query.filter_by(name=aName).all()
    aDict[aName]["OS"] = OS.query.filter_by(name=aName).all()

  return render_template("machines/machines.html", theMachines=aDict)

