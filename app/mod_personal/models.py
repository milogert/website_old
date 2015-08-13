from app import db

class Game(db.Model):
  __bind_key__ = "personal"
  __tablename__ = "Game"

  id = db.Column(db.Integer, primary_key=True, unique=True)
  name = db.Column(db.String(128))
  game_key = db.Column(db.String(512))

