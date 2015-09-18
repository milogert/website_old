#!/usr/bin/python2

from flask import Flask, render_template, url_for, redirect, request, \
                  flash, session, Blueprint, jsonify
from werkzeug import secure_filename

from forms import NewRecord, PhotoForm

# Import models.
from app.mod_vehicles.models import ServiceRecord, Vehicle
from app import db

# Create the blueprint.
mod_vehicles = Blueprint('vehicles', __name__, url_prefix="/vehicles")


@mod_vehicles.before_request
def requireAuth():
  if "username" not in session or session["username"] != "milo":
    return redirect(url_for("auth.signin"))


@mod_vehicles.route("/", methods=["GET", "POST"])
def serviceRecord():
  aForm = NewRecord()

  # get the vehicle list and put it in the choices list.
  aVehicleList = Vehicle.query.all()
  aForm.vehicle.choices = [(str(x.id), x.make + " " + x.model) for x in aVehicleList]

  if aForm.validate_on_submit():
    aRecord = ServiceRecord(
      aForm.date.data,
      aForm.vehicle.data,
      aForm.miles.data,
      aForm.description.data
    )

    db.session.add(aRecord)
    db.session.commit()

    # Create the correct directory.
    import os
    os.makedirs("app/static/vehicles/receipts/" + str(aRecord.id))

    flash("Record added", "success")

    # Reset the form.
    aForm = NewRecord()

  # Get the service record list.
  aRecordList = map(
    lambda x: {
      "id": x[0].id,
      "make": x[1].make,
      "model": x[1].model,
      "date": x[0].date,
      "miles": x[0].miles,
      "description": x[0].description
    },
    db.session.query(ServiceRecord, Vehicle).join(Vehicle).order_by(ServiceRecord.date.desc()).all()
  )

  return render_template(
    "vehicles/service.html",
    theRecords=aRecordList,
    theVL=aVehicleList,
    theForm=aForm
  )


@mod_vehicles.route("/print/<int:theId>/")
def printRecord(theId):
  """Produce a nice page for printing."""

  aVehicle = Vehicle.query.filter_by(id=theId).first()

  # Get the record.
  import os
  aRows = map(
    lambda x: {
      "id": x[0].id,
      "make": x[1].make,
      "model": x[1].model,
      "date": x[0].date,
      "miles": x[0].miles,
      "description": x[0].description,
      "photos": [url_for("static", filename="vehicles/receipts/" + str(x[0].id) + "/" + y) for y in os.listdir("app/static/vehicles/receipts/" + str(x[0].id))]

    },
    db.session.query(ServiceRecord, Vehicle).filter_by(vehicle=theId).join(Vehicle).order_by(ServiceRecord.date.desc()).all()
  )

  return render_template(
    "vehicles/print.html",
    theVehicle=aVehicle,
    theRecords=aRows
  )


@mod_vehicles.route("/record/<int:theId>/", methods=["GET", "POST"])
def specificRecord(theId):
  # Get the record.
  aRow = db.session.query(ServiceRecord, Vehicle).filter_by(id=theId).join(Vehicle).first()
  aRecord = {
    "id": aRow[0].id,
    "year": aRow[1].year,
    "make": aRow[1].make,
    "model": aRow[1].model,
    "date": aRow[0].date,
    "miles": aRow[0].miles,
    "description": aRow[0].description
  }

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

    flash("File uploaded", "success")

    aForm = PhotoForm()

  return render_template(
    "vehicles/record.html",
    theRecord=aRecord,
    theFiles=aList,
    theForm=aForm
  )


