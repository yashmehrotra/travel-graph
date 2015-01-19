from flask import Flask
app = Flask(__name__)

app.secret_key = 'A0Zr98j/asd R~XHH!jmN]LWX/,?RT'

import views
from apps.api import api
