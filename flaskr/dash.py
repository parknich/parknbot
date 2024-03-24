from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('queue', __name__)

# Initialize a global variable to store chatUser data
global_chatUsers = ['No chatUsers in queue']
global_response = ['No response']
global chatUserSlots
chatUserSlots = int()
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
    global global_chatUsers

    if request.method == 'POST':
        # Assuming the data is sent as a JSON array in the request
        global chatUserSlots
        chatUsers1 = request.json.get('chatUsers', [])
        print(chatUsers1)
        chatUserSlots = int(request.json.get('chatUserSlots'))
        # Update the global variable with the received data
        if not chatUsers1:
            chatUsers1=['No chatUsers in queue']
            global_chatUsers = chatUsers1
        else:   
            global_chatUsers = chatUsers1
            
        for chatUser in global_chatUsers:
            print(chatUser)
            
        

        # Process the chatUsers list as needed (store in the database, etc.)

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(global_chatUsers)
        return jsonify(chatUsers=global_chatUsers, chatUserSlots=chatUserSlots)

    
    db = get_db()
    return render_template('dash/obs/queue.html', chatUsers=global_chatUsers, chatUserSlots=chatUserSlots)


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
    global chat
    global chatUser
    global chatMsg
    global chatMsgPlatform

    if request.method == 'POST':
        chatMsgPlatform = request.json.get('chatMsgPlatform', [])
        chatMsg = request.json.get('chatMsg', [])
        chatUser = request.json.get('chatUser', [])
    
        print("chatMsg: " + chatMsg)
    
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(chatMsg)
        return jsonify(chatMsg=chatMsg, chatUser=chatUser, chatMsgPlatform=chatMsgPlatform)
        
        
    
    db = get_db()
    return render_template('dash/obs/chat.html', chatMsg=chatMsg, chatUser=chatUser)

