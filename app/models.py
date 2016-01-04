from app import db,socketio
from datetime import datetime,timedelta
from sqlalchemy import desc
from flask.ext.sqlalchemy import event

class Clicker(db.Model):
    """
    Record the clicker's name, time they waited and time they clicked the button
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), index=True,unique=True)
    clicked = db.Column(db.DateTime,index=True)
    waited = db.Column(db.Interval,index=True)

    def __init__(self,username,clicked=None,waited=None):
        timestamp = datetime.utcnow()
        self.username = username
        if clicked is None:
            self.clicked = timestamp
        else:
            self.clicked = clicked
        if waited is None:
            self.waited = self.getWaitedTime(timestamp)
        else:
            self.waited = waited

    def getWaitedTime(self,my_time):
        """
        calculate the time difference between current clicker and the last one
        """
        last_click,last_clicker = get_last_click_and_clicker()
        if last_clicker is None:
            return timedelta(0)
        else:
            return my_time - last_click

@event.listens_for(Clicker,'after_insert')
def after_insert_listener(mapper,connection,target):
    socketio.emit('collective update',{'data':{'name':target.username,'time':target.clicked}})
    print "________"+target.username

def get_last_click_and_clicker():
    """
    Return (last click time, username of last clicker)
    """
    last_clicker = Clicker.query.order_by(desc(Clicker.clicked)).first()
    if last_clicker is None:
        return datetime.utcnow(), None
    return last_clicker.clicked, last_clicker.username

def get_leaders():
    return Clicker.query.order_by(Clicker.waited.desc()).all()
