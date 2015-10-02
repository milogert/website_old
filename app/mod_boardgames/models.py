# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__ = True

  id = db.Column(db.Integer, primary_key=True)


# Define a User model
class Boardgame(Base):
  __bind_key__ = "boardgames"
  __tablename__ = 'boardgame'

  name = db.Column(db.String(128), nullable=False, unique=True)
  acquired = db.Column(
    db.Enum('Amazon','FLGS','Gift','Kickstarter','Massdrop'),
    nullable=False
  )
  cost = db.Column(db.Integer, nullable=False)
  plays = db.Column(db.Integer, nullable=False)
  averageTime = db.Column(db.Float, nullable=False)
  playsLeft = db.Column(db.Integer, nullable=False, default=3)
  status = db.Column(
    db.Enum("Play Next", "Default", "Has Not Arrived", 'Donated or Sold'),
    nullable=False
  )

  def __repr__(self):
    return '<Game {} {} {} {} {} {} {}>'.format(
      self.name,
      self.acquired,
      self.cost,
      self.plays,
      self.averageTime,
      self.playsLeft,
      self.status
    )
