from flask import Flask
app = Flask(__name__)

import views
from apps.api import api
