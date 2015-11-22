import hashlib
import json
import random
import requests

from verak.models import (
    DbRequestKey,
    DbUser,
    session
)

from verak.helpers import (
    redis_client,
    response_error,
    response_unauthorised
)

from verak.settings import (
    AUTH_KEY_NAMESPACE,
    ACCESS_TOKEN_NAMESPACE,
    REDIS_AUTH_KEY_DB,
    REDIS_ACCESS_TOKEN_DB,
    FACEBOOK_GRAPH_URL
)


def generate_key():
    """
    Used to generate auth_key and access_token
    """
    key = hashlib.sha256(str(random.getrandbits(256))).hexdigest()
    return key


def generate_auth_key(request_key):
    """
    Sets auth_key in redis
    """

    redis_cli = redis_client(db=REDIS_AUTH_KEY_DB)
    auth_key = generate_key()

    request_key_obj = session.query(DbRequestKey).\
                        filter(DbRequestKey.request_key == request_key).\
                        first()

    if not request_key_obj:
        return None

    ttl = request_key_obj.ttl
    type = request_key_obj.type
    value = json.dumps({'ttl': ttl, 'type': type})
    key = AUTH_KEY_NAMESPACE + auth_key

    redis_cli.setex(key, ttl, value)

    return auth_key


def verify_auth_key(auth_key):
    """
    Verify user's auth_key
    """

    redis_cli = redis_client(db=REDIS_AUTH_KEY_DB)
    auth_key = redis_cli.get(AUTH_KEY_NAMESPACE + auth_key)

    if not auth_key:
        return response_unauthorised()

    return auth_key


def generate_access_token(user_id, auth_key):
    """
    Sets access_token in redis
    """

    redis_cli = redis_client(db=REDIS_ACCESS_TOKEN_DB)

    auth_key_verified = verify_auth_key(auth_key)
    ttl = json.loads(auth_key_verified)['ttl']

    access_token = generate_key()

    value = {
        'user_id': user_id,
        'ttl': ttl
    }

    value = json.dumps(value)
    key = ACCESS_TOKEN_NAMESPACE + access_token

    redis_cli.setex(key, ttl, value)
    return access_token


def verify_access_token(access_token):
    """
    Verify user's access_token and also return user_id
    """

    redis_cli = redis_client(db=REDIS_ACCESS_TOKEN_DB)
    access_token = redis_cli.get(ACCESS_TOKEN_NAMESPACE + access_token)

    if not access_token:
        return False

    acc_tok_obj = json.loads(access_token)

    return acc_tok_obj


def refresh_key(key):
    """
    Refreshes auth_key or access_token
    """

    if AUTH_KEY_NAMESPACE in key:
        redis_db = REDIS_AUTH_KEY_DB
    elif ACCESS_TOKEN_NAMESPACE in key:
        redis_db = REDIS_ACCESS_TOKEN_DB
    else:
        return False

    redis_cli = redis_client(db=redis_db)
    value = redis_cli.get(key)
    ttl = json.loads(value)['ttl']
    # Delete key and make a new key
    redis_cli.setex(key, ttl, value)


def generate_username(first_name, last_name):
    """
    Generating unique usernames
    """

    username = u'{0}-{1}-'.format(first_name.lower(), last_name.lower())

    count_uname = session.query(DbUser).\
                    filter(DbUser.username.startswith(username)).\
                    count()

    user_nth = count_uname + 1
    username += unicode(user_nth)

    return username


def destroy_access_token(access_token):
    """
    Destroys the given access token
    """

    redis_cli = redis_client(db=REDIS_ACCESS_TOKEN_DB)
    keys_deleted = redis_cli.delete(access_token)

    return keys_deleted


def verify_facebook_auth(fb_acc_token, fb_user_id, email):
    """
    Checks whether the email provided matches the
    user's actual email
    """

    url = FACEBOOK_GRAPH_URL + fb_user_id + '?access_token=' + fb_acc_token
    fb_resp = requests.get(url).json()

    if email != fb_resp['email']:
        return response_error("Unauthenticated Request")

    return True


def get_facebook_picture(fb_acc_token, fb_user_id, height='256', width='256'):
    """
    Gets user's facebook profile picture
    """

    url = "{0}{1}/picture?redirect=false"\
          "&access_token={2}&height={3}&width={4}".format(FACEBOOK_GRAPH_URL,
                                                          fb_user_id,
                                                          fb_acc_token,
                                                          height,
                                                          width)

    fb_resp = requests.get(url).json()

    if fb_resp['data']['is_silhouette']:
        return None

    return fb_resp['data']['url']
