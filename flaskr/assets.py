from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import json
bp = Blueprint('queue', __name__)

# Pages
@bp.route('/assets/<path:path>', methods=('GET', 'POST'))
def sendAssets(path):
    db = get_db()
    return send_from_directory('assets', path)

