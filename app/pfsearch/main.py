#!/usr/bin/python2

from flask import Flask, render_template, url_for, redirect, request, flash, session, Blueprint
from flask.ext.mail import Mail, Message
from flask.ext.mongoengine import MongoEngine
import hashlib
import model
import os
import re
import shutil
import subprocess
import time

from db import Spell


pfsearch = Blueprint(
  'pfsearch',
  __name__,
  static_folder='../static/pfsearch',
  template_folder='../templates/pfsearch'
)

@pfsearch.route('/')
def index():
  return render_template("index.html")


@pfsearch.route("/test")
def test():
  a = []
  for spell in Spell.objects:
    print ">" + spell.school + "<"

  return render_template("test.html", test=a)
