from flask import Flask, render_template, request, send_from_directory

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import CsrfProtect

# Create the application.
app = Flask(__name__)

# Config file.
app.config.from_object("config")

# Enable the SQLAlchemy database.
db = SQLAlchemy(app)

# Setup CSRF protection (for forms).
csrf = CsrfProtect(app)

# Serve static files that help indexers.
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
  return send_from_directory(app.static_folder, request.path[1:])

# Error page handling.
@app.errorhandler(404)
def not_found(error):
  return render_template('status/404.html'), 404

@app.errorhandler(405)
def not_allowed(error):
  return render_template('status/405.html'), 405

@csrf.error_handler
def csrf_error(error):
  return render_template("status/csrf.html", theError=error), 400

# Import and create blueprint modules.
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_boardgames.controllers import mod_boardgames as boardgames_module
from app.mod_iacl.controllers import mod_iacl as iacl_module
from app.mod_machines.controllers import mod_machines as machines_module
from app.mod_personal.controllers import mod_personal as personal_module
from app.mod_throne_magic.controllers import mod_throne_magic as throne_magic_module
from app.mod_vehicles.controllers import mod_vehicles as vehicles_module

# Register blueprint.
app.register_blueprint(auth_module)
app.register_blueprint(boardgames_module)
app.register_blueprint(iacl_module)
app.register_blueprint(machines_module)
app.register_blueprint(personal_module)
app.register_blueprint(throne_magic_module)
app.register_blueprint(vehicles_module)


## Template functions. ########################################################

# Get the ip address for the colored navbar.
@app.template_global("ipColor")
def ipColor():
  # Get the ip address of the client.
  ip = request.environ['REMOTE_ADDR']

  # Get the list of 4 elements each.
  s = "".join(x.zfill(3) for x in ip.split("."))
  t = [(int(s[i:i + 4]) % 128) + 128 for i in range(0, len(s), 4)]

  # Return the tuple.
  return t


# Set up debugging code.
@app.template_global("debug")
def debug():
  # Get the domain name.
  h = request.host

  # Get either the port or the subdomain.
  return True if h.split(".")[0] == "dev" or h.split(":")[-1] == "5000" else False
###############################################################################

