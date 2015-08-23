from flask import Blueprint, request

from verak.models import (
    DbEmailInvite,
    DbRequestKey,
    DbUser,
    DbUserFollowing,
    session
)

from verak.redirects import URL_HOME
from verak.helpers import (
    response_json,
    response_error
)

from verak.decorators import (
    auth_required,
    login_required
)

from verak.user.utils import (
    destroy_access_token,
    generate_auth_key,
    generate_access_token,
    generate_username,
    verify_facebook_auth
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
        fb_acc_tok = request.form['fb_acc_tok']
        fb_user_id = request.form['fb_user_id']
        auth_key = request.headers['auth_key']

    except KeyError:
        response = {
            'status': 'failed',
            'error': 'please provide first_name, last_name and email'
        }

        return response_json(response, status=400)

    verify_facebook_auth(fb_acc_tok, fb_user_id, email)

    # Check whether email is unique
    existing_user = session.query(DbUser).\
                        filter(DbUser.email == email).\
                        first()

    if existing_user:
        # Log that asshole in
        access_token = generate_access_token(existing_user.id, auth_key)

        response = {
            'status': 'success',
            'user_id': existing_user.id,
            'access_token': access_token,
            'redirect_url': URL_HOME
        }

        return response_json(response)

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

    if not auth_key:
        return response_error('Invalid request key')

    response = {
        'status': 'success',
        'auth_key': auth_key
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


@api_user.route('/logout/', methods=['GET'])
@auth_required
@login_required
def user_logout_view():
    """
    Logs user out, destorys his access token
    """

    destroy_access_token(request.headers['access_token'])

    response = {
        'status': 'success',
        'message': 'Log out Successful'
    }

    return response_json(response)


@api_user.route('/follow/', methods=['POST'])
@auth_required
@login_required
def user_follow_view(user_id=None):
    """
    To follow a user id
    """

    following_id = request.form.get('following_id')

    if not following_id:
        return response_error('Missing Parameters')

    follower_id = request.user_id

    if following_id == follower_id:
        return response_error('You cannot follow yourself')

    relation_exists = session.query(DbUserFollowing).\
                        filter(DbUserFollowing.follower_id == follower_id,
                               DbUserFollowing.following_id == following_id).\
                        first()

    if relation_exists:
        """
        The given user_ids have
        an existing relationship
        """
        if relation_exists.enabled:
            """
            Follower is already following
            """

            return response_error("User already follows the given user")

        else:
            """
            Changing enabled flag to False
            """

            relation_exists.enabled = True
            session.add(relation_exists)
            session.commit()

            response = {
                'status': 'success',
                'message': 'User {0} is now following User {1}'.\
                                format(follower_id, following_id)
            }

            return response_json(response)

    else:
        """
        Create a new relation
        """

        new_relation = DbUserFollowing(follower_id=follower_id,
                                       following_id=following_id)
        session.add(new_relation)
        session.commit()

        response = {
            'status': 'success',
            'message': 'User {0} is now following User {1}'.\
                            format(follower_id, following_id)
        }

        return response_json(response)


@api_user.route('/unfollow/', methods=['POST'])
@auth_required
@login_required
def unfollow_user_view():
    """
    To unfollow a user
    """

    follower_id = request.user_id
    following_id = request.form.get('following_id')

    if not following_id:
        return response_error('Missing Parameters')

    relation = session.query(DbUserFollowing).\
                filter(DbUserFollowing.follower_id == follower_id,
                       DbUserFollowing.following_id == following_id).\
                first()

    if not relation:
        return response_error('No relationship exists')

    if not relation.enabled:
        return response_error('Already unfollowed')

    # Set the enabled flag to false
    relation.enabled = False

    session.add(relation)
    session.commit()

    response = {
        'status': 'success',
        'message': 'User {0} unfollowed User {1}'.\
                        format(follower_id, following_id)
    }

    return response_json(response)


@api_user.route('/<int:user_id>/followers/', methods=['GET'])
@auth_required
@login_required
def get_user_followers_view(user_id):
    """
    Returns a list of all the followers of a user
    """

    followers = session.query(DbUserFollowing).\
                    filter(DbUserFollowing.following_id == user_id,
                           DbUserFollowing.enabled == True)

    followers_list = []

    for f in followers:
        followers_list.append({
            'follower_id': f.follower_id,
            'following_id': f.following_id,
            'create_ts': str(f.create_ts)
        })

    response = {
        'status': 'success',
        'followers': followers_list
    }

    return response_json(response)


@api_user.route('/<int:user_id>/following/', methods=['GET'])
@auth_required
@login_required
def get_user_following_view(user_id):
    """
    Returns a list of all the people the user follows
    """

    following = session.query(DbUserFollowing).\
                    filter(DbUserFollowing.follower_id == user_id,
                           DbUserFollowing.enabled == True)

    following_list = []

    for f in following:
        following_list.append({
            'follower_id': f.follower_id,
            'following_id': f.following_id,
            'create_ts': str(f.create_ts)
        })

    response = {
        'status': 'success',
        'following': following_list
    }

    return response_json(response)
