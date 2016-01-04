#!flask/bin/python
from app import app,db,socketio

db.create_all()
socketio.run(app)
