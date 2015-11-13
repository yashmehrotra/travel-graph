from flask import Flask, request
from flask_restful import Resource
import json

from verak.user.views import api_user
from verak.development.views import developer_blueprint
from verak.doobie.views import api_question
from verak.tag.views import api_tag
from verak.search.views import search_blueprint

app = Flask(__name__)
app.secret_key = 'A0Zr98j/asd R~XHH!jmN]LWX/,?RT'

app.register_blueprint(api_user, url_prefix='/api/user')
app.register_blueprint(developer_blueprint, url_prefix='/developer')
app.register_blueprint(api_question, url_prefix='/api/question')
app.register_blueprint(api_tag, url_prefix='/api/tag')
app.register_blueprint(search_blueprint, url_prefix='/api/search')

# Adding Flask Restful endpoints
for cls in Resource.__subclasses__():
    # Iterating through all the FRF Subclasses
    api_bp = cls.api_blueprint
    api_bp.add_resource(cls, cls.url_endpoint)

# CORS Settings
ALLOWED_CORS_HEADERS = 'Content-Type, auth_key, access_token'


@app.before_request
def change_json_to_form():
    """
    Converts the incoming data from
    JSON format to form format
    """

    # We only do it when we cannot get form data
    if not request.form and request.data:
        try:
            request.form = json.loads(request.data)
        except ValueError:
            pass


@app.after_request
def add_cors(resp):
    """
    Ensure all responses have the CORS headers.
    This ensures any failures are also accessible by the client.
    """

    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Credentials'] = 'false'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET, PUT'
    resp.headers['Access-Control-Allow-Headers'] = ALLOWED_CORS_HEADERS
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp
