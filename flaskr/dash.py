from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('queue', __name__)

# Initialize a global variable to store chatUser data
global_users = ['No chatUsers in queue']
global_response = ['No response']
global userSlots
userSlots = int()
global chat
global chatMsg
global chatUser
chatUser = str()
chat = list()
chatMsg = str()
chatMsgPlatform = bool()

# Pages
@bp.route('/dash/obs/queue', methods=('GET', 'POST'))
def queue():
    global global_users

    if request.method == 'POST':
        # Assuming the data is sent as a JSON array in the request
        global userSlots
        users1 = request.json.get('chatUsers', [])
        print(users1)
        userSlots = int(request.json.get('userSlots'))
        # Update the global variable with the received data
        if not users1:
            users1=['No users in queue']
            global_users = users1
        else:   
            global_users = users1
            
        for user in global_users:
            print(chatUser)
            
        

        # Process the chatUsers list as needed (store in the database, etc.)

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(global_users)
        return jsonify(chatUsers=global_users, userSlots=userSlots)

    
    db = get_db()
    return render_template('dash/obs/queue.html', chatUsers=global_users, userSlots=userSlots)


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

        # Process the chatUsers list as needed (store in the database, etc.)

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(global_response)
        return jsonify(response=global_response)

    db = get_db()
    return render_template('dash/obs/responses.html', response=global_response)
@bp.route('/dash/obs/chat', methods=('GET', 'POST'))
def chat():
    global chatMsg

    if request.method == 'POST':
        chatMsg = request.json.get('chat', [])
        for msg in chatMsg:
            print(msg)
        
    
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(chatMsg)
        return jsonify(chatMsg=chatMsg)
        
        
    
    db = get_db()
    return render_template('dash/obs/chat.html', chatMsg=chatMsg)

