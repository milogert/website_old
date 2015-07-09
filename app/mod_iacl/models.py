# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

  __abstract__  = True

  id = db.Column(db.Integer, primary_key=True)


class Campaign(Base):
  __bind_key__ = "iacl"
  __tablename__ = "Campaign"

  code = db.Column(db.String(10), nullable=False)
  name = db.Column(db.String(128), nullable=False)
  credits = db.Column(db.Integer, default=0)

  def __repr__(self):
    return "<Campaign {} {}>".format(self.code, self.name)

class AgendaSet(Base):
  __bind_key__ = "iacl"
  __tablename__ = "AgendaSet"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  setname = db.Column(db.String(32), nullable=False)


class AgendaSub(Base):
  __bind_key__ = "iacl"
  __tablename__ = "AgendaSub"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  setname = db.Column(db.String(32), db.ForeignKey('AgendaSet.setname'), nullable=False)
  name = db.Column(db.String(32), nullable=False)
  purchased = db.Column(db.Boolean, default=False)
  active = db.Column(db.Boolean, default=False)
  discarded = db.Column(db.Boolean, default=False)


class Empire(Base):
  __bind_key__ = "iacl"
  __tablename__ = "Empire"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  cls = db.Column(db.String(32), nullable=False)
  xp = db.Column(db.Integer, default=0)
  influence = db.Column(db.Integer, default=0)


class EmpireSkill(Base):
  __bind_key__ = "iacl"
  __tablename__ = "EmpireSkill"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  cls = db.Column(db.String(32), db.ForeignKey('Empire.cls'), nullable=False)
  name = db.Column(db.String(32), nullable=False)


class Hero(Base):
  __bind_key__ = "iacl"
  __tablename__ = "Hero"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  name = db.Column(db.String(32), nullable=False)
  xp = db.Column(db.String(32), default=0)

  def __repr__(self):
    return "<Hero {} {} {}>".format(self.code, self.name, self.xp)


class HeroSkill(Base):
  __bind_key__ = "iacl"
  __tablename__ = "HeroSkill"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  name = db.Column(db.String(32), db.ForeignKey('Hero.name'), nullable=False)
  title = db.Column(db.String(32), nullable=False)

  def __repr__(self):
    return "<HeroSkill {} {} {}>".format(self.code, self.name, self.title)


class HeroGear(Base):
  __bind_key__ = "iacl"
  __tablename__ = "HeroGear"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  name = db.Column(db.String(32), nullable=False)

  def __repr__(self):
    return "<HeroGear {} {}>".format(self.code, self.name)


class Mission(Base):
  __bind_key__ = "iacl"
  __tablename__ = "Mission"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  name = db.Column(db.String(32), nullable=False)
  active = db.Column(db.Boolean, default=False)


class Reward(Base):
  __bind_key__ = "iacl"
  __tablename__ = "Reward"

  code = db.Column(db.String(10), db.ForeignKey('Campaign.code'), nullable=False)
  name = db.Column(db.String(32), nullable=False)


