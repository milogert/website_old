# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__ = True

  id = db.Column(db.Integer, primary_key=True)


class ServiceRecord(Base):
  __bind_key__ = "personal"
  __tablename__ = "ServiceRecord"

  vehicle = db.Column(
    db.Enum('Yamaha FZ-0'),
    nullable=False
  )
  date = db.Column(db.Date, nullable=False)
  miles = db.Column(db.Integer, nullable=False)
  description = db.Column(db.Text, nullable=False)

  def __init__(self, date, vehicle, miles, description):
    self.date = date
    self.vehicle = vehicle
    self.miles = miles
    self.description = description


