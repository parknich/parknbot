from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('queue', __name__)

# Initialize a global variable to store user data
global_users = ['No users in queue']

@login_required
@bp.route('/dash/obs/queue', methods=('GET', 'POST'))
def queue():
    global global_users

    if request.method == 'POST':
        # Assuming the data is sent as a JSON array in the request
        users1 = request.json.get('users', [])
        print(users1)

        # Update the global variable with the received data
        
        if not global_users:
            global_users = ['No users in queue']
        else:
            global_users = users1
            
        for user in global_users:
            print(user)

        # Process the users list as needed (store in the database, etc.)

    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(global_users)
        return jsonify(users=global_users)

    db = get_db()
    return render_template('dash/obs/queue.html', users=global_users)
