from app import app,db,socketio
from models import Clicker,get_last_click_and_clicker,get_leaders
from datetime import datetime
from flask import render_template,request,redirect,flash
from form import ClickForm
from flask.ext.socketio import emit
from api import cats_api

app.register_blueprint(cats_api)  # connects route configration in api.py

@app.route('/')
def index():
    form = ClickForm()
    last_click, last_clicker = get_last_click_and_clicker()
    delta = datetime.utcnow() - last_click
    leaders = get_leaders()
    return render_template('index.html', **locals())

@socketio.on('connected')
def confirm_connection(message):
    last_click,_ = get_last_click_and_clicker()
    emit('server confirmation',{'last':last_click})

@socketio.on('collective update')
def handler(message):
    pass


@app.route('/click', methods=['POST'])
def click_thebutton():
    """use wtforms to do validations, error handling"""
    form = ClickForm()
    if request.method=='POST' and form.validate_on_submit():
        c = Clicker(
            username=request.form['username'],
            clicked=datetime.utcnow())
        db.session.add(c)
        db.session.commit()
    else:
        flash(str(form.errors),'error')
        print str(form.errors)
    # FIXME: handle and report errors
    return redirect('/')
