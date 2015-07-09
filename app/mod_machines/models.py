# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__ = True

  id = db.Column(db.Integer, primary_key=True)


# Define a User model
class Spec(Base):
  __bind_key__ = "machines"
  __tablename__ = "spec"

  name = db.Column(db.String(128), nullable=False, unique=True)
  acquired = db.Column(
    db.Enum('Amazon','FLGS','Gift','Kickstarter','Massdrop'),
    nullable=False
  )
  manufacturer = db.Column(db.String(1024))
  model = db.Column(db.String(1024))
  comp_case = db.Column(db.String(1024))
  motherboard = db.Column(db.String(1024))
  processor = db.Column(db.String(1024))
  memory = db.Column(db.String(1024))
  video = db.Column(db.String(1024))
  audio = db.Column(db.String(1024))
  psu = db.Column(db.String(1024))


class OS(Base):
  __bind_key__ = "machines"
  __tablename__ = "os"

  name = db.Column(
    db.String(128),
    db.ForeignKey('Spec.name'),
    nullable=False,
    unique=True
  )
  os = db.Column(db.String(1024), nullable=False)


class Drive(Base):
  __bind_key__ = "machines"
  __tablename__ = "drive"

  name = db.Column(
    db.String(128),
    db.ForeignKey('Spec.name'),
    nullable=False,
    unique=True
  )
  type = db.Column(
    db.Enum("SSD", "HDD", "Optical"),
    nullable=False
  )
  size = db.Column(db.Integer)
  make = db.Column(db.String(1024))
  model = db.Column(db.String(1024))
  use = db.Column(
    db.Enum("Primary", "Storage"),
    nullable=False
  )


class Display(Base):
  __bind_key__ = "machines"
  __tablename__ = "display"

  name = db.Column(
    db.String(128),
    db.ForeignKey('Spec.name'),
    nullable=False,
    unique=True
  )
  size = db.Column(db.Integer)
  make = db.Column(db.String(1024))
  model = db.Column(db.String(1024))

