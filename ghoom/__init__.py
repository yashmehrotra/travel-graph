from flask import Flask
# from werkzeug.contrib.fixers import ProxyFix
from ghoom.user.views import api
from ghoom.development.views import developer

app = Flask(__name__)

app.secret_key = 'A0Zr98j/asd R~XHH!jmN]LWX/,?RT'
# app.wsgi_app = ProxyFix(app.wsgi_app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(developer, url_prefix='/developer')
