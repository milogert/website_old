#!/usr/bin/python2

import os, sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if path not in sys.path:
  sys.path.insert(0, "/srv/http")

from main import app as application
