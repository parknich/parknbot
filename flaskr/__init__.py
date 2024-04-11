import os

from flask import Flask, Response, jsonify, request, send_file
from flask_migrate import Migrate
import requests
from . import db
from . import auth
from . import news
from . import dash
from . import assets
import ssl
context = ssl.SSLContext()
context.load_cert_chain('/etc/letsencrypt/live/parknbot.xyz/fullchain.pem', '/etc/letsencrypt/live/parknbot.xyz/privkey.pem')
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        
    @app.route('/twitch-callback',methods=['GET'])
    def proxy():
        if request.method=='GET':
            resp = requests.get(f'127.0.0.1:4000')
            excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
            headers = [(name, value) for (name, value) in     resp.raw.headers.items() if name.lower() not in excluded_headers]
            response = Response(resp.content, resp.status_code, headers)
            
        return response
    app.register_blueprint(auth.bp)
    app.register_blueprint(dash.bp)
    app.register_blueprint(news.bp)
    app.register_blueprint(assets.bp)
    app.add_url_rule('/', endpoint='index')

    migrate = Migrate(app, db) 
    db.init_app(app)

    return app