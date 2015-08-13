# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):
  __abstract__ = True

  id = db.Column(db.Integer, primary_key=True)


# Define a User model
class Core(Base):
  __bind_key__ = "resume"
  __tablename__ = "Core"

  name = db.Column(db.String(128), nullable=False)
  address = db.Column(db.String(128), nullable=False)
  city = db.Column(db.String(128), nullable=False)
  state = db.Column(db.String(2), nullable=False)
  zipc = db.Column(db.String(10), nullable=False)
  phone = db.Column(db.String(16), nullable=False)
  email = db.Column(db.String(128), nullable=False)
  objective = db.Column(db.String(1024), nullable=False)

  def __repr__(self):
    return "<Core {} {} {} {}>".format(self.name, self.address, self.phone, self.email)


class Job(Base):
  __bind_key__ = "resume"
  __tablename__ = "Job"

  company = db.Column(db.String(128), nullable=False)
  city = db.Column(db.String(128), nullable=False)
  state = db.Column(db.String(2), nullable=False)
  title = db.Column(db.String(128), nullable=False)
  start = db.Column(db.Date)
  end = db.Column(db.Date, nullable=True)

  def __repr__(self):
    return "<Job {} {}>".format(self.company, self.start)


class JobDuty(Base):
  __bind_key__ = "resume"
  __tablename__ = "JobDuty"

  companyid = db.Column(db.Integer, db.ForeignKey("Job.id"), nullable=False)
  duty = db.Column(db.String(1024), nullable=False)

  def __repr__(self):
    return "<Duty {} {}>".format(self.companyid, self.duty)


class SkillCategory(Base):
  __bind_key__ = "resume"
  __tablename__ = "SkillCategory"

  name = db.Column(db.String(128), nullable=False)


class Skill(Base):
  __bind_key__ = "resume"
  __tablename__ = "Skill"

  categoryid = db.Column(db.Integer, db.ForeignKey("SkillCategory.id"), nullable=False)
  name = db.Column(db.String(128), nullable=False)


class Award(Base):
  __bind_key__ = "resume"
  __tablename__ = "Award"

  name = db.Column(db.String(512), nullable=False)


class Education(Base):
  __bind_key__ = "resume"
  __tablename__ = "Education"

  name = db.Column(db.String(128))
  city = db.Column(db.String(128))
  state = db.Column(db.String(128))
  degree = db.Column(db.String(128))
  grad = db.Column(db.Boolean)
  start = db.Column(db.Date)
  end = db.Column(db.Date, nullable=True)
  note = db.Column(db.Text, nullable=True)

