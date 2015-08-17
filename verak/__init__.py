from flask import Flask
from flask.ext.cors import CORS
# from werkzeug.contrib.fixers import ProxyFix
from verak.user.views import api_user
from verak.development.views import developer
from verak.doobie.views import api_question

app = Flask(__name__)
# For allowing Cross-Origin-Resource Sharing
# Should not go into production
# Research about it
CORS(app)
app.secret_key = 'A0Zr98j/asd R~XHH!jmN]LWX/,?RT'
# app.wsgi_app = ProxyFix(app.wsgi_app)

app.register_blueprint(api_user, url_prefix='/api/user')
app.register_blueprint(developer, url_prefix='/developer')
app.register_blueprint(api_question, url_prefix='/api/question')
