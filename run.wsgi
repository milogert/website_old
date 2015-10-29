#!/usr/bin/python2

import os, sys

# Get the current directory for the absolute path.
path = os.path.dirname(os.path.abspath(__file__))

# Set the path to activate this.
activate_this = path + "/env/bin/activate_this.py"

# Exec the file.
execfile(activate_this, dict(__file__=activate_this))

# Add the dir to the python path.
sys.path.insert(0, path)

# Import the app.
from app import app as application

