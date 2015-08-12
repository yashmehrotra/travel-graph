from flask import Blueprint, request

from ghoom.models import (
    DbEmailInvite,
    DbUser,
    session
)

from ghoom.helpers import response_json
from ghoom.decorators import (
    auth_required,
    login_required
)

from ghoom.user.utils import (
    generate_auth_key,
    generate_access_token
)

api = Blueprint('api', __name__)


@auth_required
@api.route('/user/<user_id>', methods=['GET', 'POST', 'PUT'])
def user_view(user_id=None):
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


@api.route('/user/auth_key/', methods=['GET'])
def auth_key_view():
    """
    Generate auth key for a user
    """

    req_key = request.args.get('req_key')
    if not req_key:
        response = {
            'status': 'failed',
            'error': 'Request Key not Provided',
        }
        return response_json(response, status=400)

    auth_key = generate_auth_key(req_key)

    response = {
        'status': 'success',
        'auth_key': auth_key
    }

    return response_json(response)


@auth_required
@api.route('/user/access_token/', methods=['GET'])
def access_token_view():
    """
    Generates access_token for user
    """

    user_id = request.args.get('user_id')
    auth_key = request.headers['auth_key']

    if not user_id:
        response = {
            'status': 'failed',
            'error': 'user_id not provided'
        }
        return response_json(response, status=400)

    access_token = generate_access_token(user_id, auth_key)

    response = {
        'status': 'success',
        'access_token': access_token
    }

    return response_json(response)


@api.route('/user/invite/email', methods=['GET', 'POST'])
def invite_email_view():
    """
    Methods related to invitation system
    """
    if request.method == 'GET':
        """
        Returns a list of allowed emails for signup
        """
        emails = session.query(DbEmailInvite.email).\
                    filter(DbEmailInvite.invited == True)

        response = {
            'status': 'success',
            'emails': emails
        }

        return response_json(response)

    elif request.method == 'POST':
        """
        Add the email to invitation pending emails
        """

        email = request.form.get('email')
        if not email:
            response = {
                'status': 'failed',
                'error': 'email not provided'
            }
            return response_json(response, status=400)

        email = email.strip().lower()

        email_count = session.query(DbEmailInvite.email).\
                        filter(DbEmailInvite.email == email).\
                        count()

        if email_count > 0:
            response = {
                'status': 'failed',
                'error': 'email already exists'
            }
            return response_json(response, status=400)

        new_invite = DbEmailInvite(email=email)

        session.add(new_invite)
        session.commit()

        response = {
            'status': 'success',
            'message': 'invitation pending'
        }

        return response_json(response)
