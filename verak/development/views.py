from flask import Blueprint, request
from flask_restful import Api, Resource

from verak.user.utils import (
    generate_auth_key,
    generate_access_token,
    generate_username
)

from verak.models import (
    DbRequestKey,
    DbUser,
    session
)

from verak.helpers import response_json

developer_blueprint = Blueprint('developer', __name__)
api_developer = Api(developer_blueprint)


class DeveloperInitFRFTest(Resource):
    """
    Made for instantly making an account
    """

    def post(self):
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        username = generate_username(first_name, last_name)

        user = DbUser(username=username,
                      email=email,
                      first_name=first_name,
                      last_name=last_name)

        session.add(user)
        session.commit()

        req_key_ttl = 60 * 60 * 24 * 31
        req_key_obj = DbRequestKey(request_key="SUPERDBADMIN",
                                   type="development",
                                   ttl=req_key_ttl)
        session.add(req_key_obj)
        session.commit()

        auth_key = generate_auth_key(req_key_obj.request_key)
        access_token = generate_access_token(user.id, auth_key)

        response = {
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            },
            'auth_key': auth_key,
            'access_token': access_token
        }

        return response_json(response)

api_developer.add_resource(DeveloperInitFRFTest, '/init/')
