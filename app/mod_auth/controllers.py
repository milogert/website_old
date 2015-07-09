# Import flask dependencies
import flask
from flask import Blueprint, request, render_template, flash, g, session, \
                  redirect, url_for, jsonify

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db#, redirect_back, get_redirect_target

# Import module forms
from app.mod_auth.forms import LoginForm

# Import module models (i.e. User)
from app.mod_auth.models import User

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth')


# Set the route and accepted methods
@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():
  # If sign in form is submitted
  form = LoginForm(request.form)

  # Verify the sign in form
  if form.validate_on_submit():

    # Get the user from the database.
    user = User.query.filter_by(name=form.username.data).first()

    # Check to see if the passwords match.
    if user and check_password_hash(user.password, form.password.data):

      # Set the session up.
      session["user_id"] = user.id
      session["username"] = user.name
      session["valid"] = True

      flash('Welcome {}'.format(user.name), "success")

      return redirect(url_for("personal.index"))

    flash('Wrong username or password', 'warning')

  return render_template("auth/signin.html", form=form)#, n=n)


@mod_auth.route("/signout/")
def signout():
  # Flash a message.
  flash("Goodbye, {}".format(session["username"]), "success")

  # Remote the items from the session.
  session.clear()

  # Redirect to another place.
  return redirect(url_for("personal.index"))


@mod_auth.route("/session/")
def getSession():
  if session["valid"]:
    return jsonify(**session)
