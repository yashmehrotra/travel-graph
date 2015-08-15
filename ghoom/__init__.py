from flask import Flask
# from werkzeug.contrib.fixers import ProxyFix
from ghoom.user.views import api_user
from ghoom.development.views import developer
from ghoom.doobie.views import api_question

app = Flask(__name__)

app.secret_key = 'A0Zr98j/asd R~XHH!jmN]LWX/,?RT'
# app.wsgi_app = ProxyFix(app.wsgi_app)

app.register_blueprint(api_user, url_prefix='/api/user')
app.register_blueprint(developer, url_prefix='/developer')
app.register_blueprint(api_question, url_prefix='/api/question')
