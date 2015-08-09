from flask import Flask
#from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

app.secret_key = 'A0Zr98j/asd R~XHH!jmN]LWX/,?RT'
#app.wsgi_app = ProxyFix(app.wsgi_app)

import views
from apps.api import api_content, api_users, api_invites

