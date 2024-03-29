from flask.ext.wtf import Form
from wtforms import DateField, SelectField, IntegerField, TextAreaField
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired


class NewRecord(Form):

  date = DateField("Date")
  vehicle = SelectField("Vehicle", choices=[])
  miles = IntegerField("Miles")
  description = TextAreaField("Description")


class PhotoForm(Form):

  upload = FileField(
    "photo",
    validators=[
      FileRequired(),
      FileAllowed(["jpeg", "jpg", "png", "gif"], "Images only!")
    ]
  )

