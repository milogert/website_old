# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__ = True

  id = db.Column(db.Integer, primary_key=True)


class Vehicle(Base):
  __bind_key__ = "vehicle"
  __tablename__ = "Vehicle"

  make = db.Column(db.Text, nullable=False)
  model = db.Column(db.Text, nullable=False)
  year = db.Column(db.Text, nullable=False)

  vehicleR = db.relationship(
    "ServiceRecord",
    backref="ServiceRecord.vehicle",
    primaryjoin="Vehicle.id==ServiceRecord.vehicle",
    lazy="joined"
  )


class ServiceRecord(Base):
  __bind_key__ = "vehicle"
  __tablename__ = "ServiceRecord"

  vehicle = db.Column(db.Integer, db.ForeignKey("Vehicle.id"), nullable=False)
  date = db.Column(db.Date, nullable=False)
  miles = db.Column(db.Integer, nullable=False)
  description = db.Column(db.Text, nullable=False)

  vehicleR = db.relationship("Vehicle", foreign_keys="ServiceRecord.vehicle")

  def __init__(self, date, vehicle, miles, description):
    self.date = date
    self.vehicle = vehicle
    self.miles = miles
    self.description = description


