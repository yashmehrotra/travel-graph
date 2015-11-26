from flask import Flask, request, jsonify, Blueprint
from flask_restful import Resource, Api
import json

from verak.user.views import api_user
from verak.doobie.views import api_question
from verak.tag.views import api_tag

from verak.development.views import Resource
from verak.search.views import Resource

from verak.decorators import (
    auth_required,
    login_required
)
app = Flask(__name__)
app.secret_key = 'A0Zr98j/asd R~XHH!jmN]LWX/,?RT'

api_bpf = Blueprint('Baba', __name__)

# Adding Flask Restful endpoints
# Iterating through all the FRF Subclasses
for cls in Resource.__subclasses__():
    # Automatic authentication decorators
    if getattr(cls, 'auth', False):
        setattr(cls, 'method_decorators', [auth_required, login_required])

    # Registering the endpoints
    endpoint = cls.url_endpoint
    if type(endpoint) != list:
        endpoint = [endpoint]

    Api(api_bpf).add_resource(cls, *endpoint)
    print 'Registed: ' + str(endpoint)

# Registering all the blueprints
app.register_blueprint(api_user, url_prefix='/api/user')
app.register_blueprint(api_question, url_prefix='/api/question')
app.register_blueprint(api_tag, url_prefix='/api/tag')
app.register_blueprint(api_bpf, url_prefix='/api')


# CORS Settings
ALLOWED_CORS_HEADERS = 'Content-Type, Auth-Key, Access-Token'


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


@app.route('/api', strict_slashes=False)
def status():
    return jsonify(message="May the force be with you")
