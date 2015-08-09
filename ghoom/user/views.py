from flask import Blueprint, request

from ghoom.models import (
    DbUser
)

api = Blueprint('api', __name__)


@api.route('/user/<user_id>', methods=['GET', 'POST', 'PUT'])
def rest_user(user_id=None):
    if request.method == 'GET':
        if user_id:
            # Serialize user, add params for all data,meta data etc.
            user = session.query(DbUser).get(user_id)
            return user
        else:
            return None
    elif request.method == 'POST':
        # Take all the params and add a new user
        return None
    elif request.method == 'PUT':
        # Edit the user
        return None
