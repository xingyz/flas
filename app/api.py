from app import app
from flask import Blueprint,jsonify
from models import get_leaders

cats_api = Blueprint('cats_api',__name__)

#list
@cats_api.route('/api/v1/cats',methods=['GET'])
def get_cats():
    users = get_leaders()
    users_list = []
    for user in users:
        users_list.append({'name':user.username,
                           'click_time':str(user.clicked),
                           'waited_time':str(user.waited)})
    print users_list
    return jsonify({'cats':users_list})

# To Do: Get Single Clicker, Add a Clicker, Secure API
