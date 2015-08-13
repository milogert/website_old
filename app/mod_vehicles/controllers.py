#!/usr/bin/python2

from flask import Flask, render_template, url_for, redirect, request, \
                  flash, session, Blueprint, jsonify
from werkzeug import secure_filename

from forms import NewRecord, PhotoForm

# Import models.
from app.mod_vehicles.models import ServiceRecord
from app import db

# Create the blueprint.
mod_vehicles = Blueprint('vehicles', __name__, url_prefix="/vehicles")


@mod_vehicles.before_request
def requireAuth():
  if "username" not in session or session["username"] != "milo":
    return redirect(url_for("auth.signin"))


@mod_vehicles.route("/sr/", methods=["GET", "POST"])
def serviceRecord():
  aForm = NewRecord()

  if aForm.validate_on_submit():
    aRecord = ServiceRecord(
      aForm.date.data,
      aForm.vehicle.data,
      aForm.miles.data,
      aForm.description.data
    )

    db.session.add(aRecord)
    db.session.commit()

  return render_template(
    "vehicles/service.html",
    theRecords=ServiceRecord.query.order_by(ServiceRecord.date.desc()).all(),
    theForm=aForm
  )


@mod_vehicles.route("/sr/<int:theId>/", methods=["GET", "POST"])
def specificRecord(theId):
  # Get the record.
  aRecord = ServiceRecord.query.filter_by(id=theId).first()

  # Get the filepaths for the photos.
  import os
  aPostfix = "vehicles/receipts/{}".format(theId)
  aList = [url_for("static", filename=aPostfix + os.sep + x) for x in os.listdir("app/static/" + aPostfix)]

  # Create the form.
  aForm = PhotoForm()

  # Check to see if the form is valid as well as a post request.
  if aForm.validate_on_submit():
    filename = secure_filename(aForm.upload.data.filename)
    aSavePath = 'app/static/vehicles/receipts/{}/'.format(theId) + filename
    aForm.upload.data.save(aSavePath)

    # Convert the photo to nice web stuff.
    from pgmagick import Image, InterlaceType
    aImg = Image(aSavePath)
    aImg.quality(80)
    aImg.scale("80%")
    aImg.interlaceType(InterlaceType.PlaneInterlace)
    aImg.write(aSavePath)

    flash("File uploaded.", "success")

  return render_template(
    "vehicles/record.html",
    theRecord=aRecord,
    theFiles=aList,
    theForm=aForm
  )


