from flask import Blueprint, request

from verak.models import (
    DbEmailInvite,
    DbRequestKey,
    DbUser,
    session
)

from verak.redirects import URL_HOME
from verak.helpers import response_json
from verak.decorators import (
    auth_required,
    login_required
)

from verak.user.utils import (
    generate_auth_key,
    generate_access_token,
    generate_username
)

api_user = Blueprint('api', __name__)


@api_user.route('/<user_id>', methods=['GET', 'PUT'])
@auth_required
@login_required
def user_view(user_id=None):
    if request.method == 'GET':
        if user_id:
            # Check if user is himself, serialize based on that
            # Serialize user, add params for all data,meta data etc.
            user = session.query(DbUser).get(user_id)
            return response_json(user.serialize)
        else:
            return None
    elif request.method == 'PUT':
        # Edit the user
        return None


@api_user.route('/', methods=['POST'])
@auth_required
def user_post_view():
    """
    To create a new user
    """

    try:

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        auth_key = request.headers['auth_key']

    except KeyError:
        response = {
            'status': 'failed',
            'error': 'please provide first_name, last_name and email'
        }

        return response_json(response, status=400)

    # Check whether email is unique
    existing_user = session.query(DbUser).\
                        filter(DbUser.email == email).\
                        first()

    if existing_user:
        # Log that asshole in
        response = {
            'status': 'failed',
            'error': 'email already exists',
            'payload': {
                'user_id': existing_user.id
            }
        }
        return response_json(response, status=400)

    profile_photo = request.form.get('profile_photo')
    facebook_token = request.form.get('facebook_token')
    google_token = request.form.get('google_token')

    username = generate_username(first_name, last_name)

    user = DbUser(username=username,
                  email=email,
                  first_name=first_name,
                  last_name=last_name,
                  profile_photo=profile_photo,
                  facebook_token=facebook_token,
                  google_token=google_token)

    session.add(user)
    session.commit()

    access_token = generate_access_token(user.id, auth_key)

    response = {
        'status': 'success',
        'user_id': user.id,
        'access_token': access_token,
        'redirect_url': URL_HOME
    }

    return response_json(response)


@api_user.route('/request_key/', methods=['GET'])
def request_key_view():
    """
    Return request key to client
    """
    req_key = session.query(DbRequestKey).first().request_key

    response = {
        'status': 'success',
        'req_key': req_key
    }

    return response_json(response)


@api_user.route('/auth_key/', methods=['GET'])
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


@api_user.route('/access_token/', methods=['GET'])
@auth_required
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


@api_user.route('/invite/email', methods=['GET', 'POST'])
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


@api_user.route('/follow/', methods=['GET', 'POST', 'PUT'])
@api_user.route('/follow/<user_id>', methods=['GET', 'PUT'])
@auth_required
@login_required
def user_follow_view(user_id=None):
    pass
