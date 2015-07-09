from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired


class PhotoForm(Form):

  upload = FileField(
    "photo",
    validators=[
      FileRequired(),
      FileAllowed(["jpeg", "jpg", "png", "gif"], "Images only!")
    ]
  )
