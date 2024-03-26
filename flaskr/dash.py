from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import lib2.twitchbadges2 as twitchbadges
import json
bp = Blueprint('queue', __name__)

# Initialize a global variable to store chatListUser data
global_users = ['No users in queue']
global_response = ['No response']
global userSlots
userSlots = int()
global chatList
global badges
badges = dict()
badges = str()
chatList = list()

# Pages
@bp.route('/dash/obs/queue', methods=('GET', 'POST'))
def queue():
    global global_users

    if request.method == 'POST':
        # Assuming the data is sent as a JSON array in the request
        global userSlots
        users1 = request.json.get('users', [])
        print(users1)
        userSlots = int(request.json.get('userSlots'))
        # Update the global variable with the received data
        if not users1:
            users1=['No users in queue']
            global_users = users1
        else:   
            global_users = users1
            
        for user in global_users:
            print(user)
            
        

        # Process the users list as needed (store in the database, etc.)

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(global_users)
        return jsonify(users=global_users, userSlots=userSlots)

    
    db = get_db()
    return render_template('dash/obs/queue.html', users=global_users, userSlots=userSlots)


@bp.route('/dash/obs/responses', methods=('GET', 'POST'))
def responses():
    global global_response

    if request.method == 'POST':
        # Assuming the data is sent as a JSON array in the request
        response1 = request.json.get('response', [])
        print(response1)

        # Update the global variable with the received data
        
        global_response = response1
            
        for response in global_response:
            print(response)

        # Process the users list as needed (store in the database, etc.)

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(global_response)
        return jsonify(response=global_response)

    db = get_db()
    return render_template('dash/obs/responses.html', response=global_response)
@bp.route('/dash/obs/chat', methods=('GET', 'POST'))
def chat():
    global chatList
    global badges

    badges = json.loads(twitchbadges.get_badge_json())
    if request.method == 'POST':
        chatList = request.json.get('chat', [])

    
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(chatList=chatList)
        
        
    
    db = get_db()
    return render_template('dash/obs/chat.html', chatList=chatList, badges=badges)

