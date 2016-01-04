
from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
socketio = SocketIO(app)
app.debug = True


# import at the end in order to avoid cross-reference error
from app import routes
