from flask.ext.wtf import Form
from wtforms import StringField, validators
from validators import Unique
from models import Clicker

# Remember to add WSRF to config.py.
class ClickForm(Form):
    # unique validator did not work!!!!!!!!!
    username = StringField('username',[validators.DataRequired()])
