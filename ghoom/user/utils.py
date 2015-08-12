import hashlib
import json
import random

from ghoom.models import (
    DbRequestKey,
    session
)

from ghoom.helpers import (
    redis_client,
    response_json,
    response_unauthorised
)

from ghoom.settings import (
    AUTH_KEY_NAMESPACE,
    ACCESS_TOKEN_NAMESPACE,
    REDIS_AUTH_KEY_DB,
    REDIS_ACCESS_TOKEN_DB
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
        resp = {
            'status': 'failed',
            'error': 'request_key not found'
        }
        return response_json(resp, status=404)

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
        response = {
            'status': 'failed',
            'error': 'Not Authorised'
        }

        return response_json(data=response,
                             status=401)

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
        return response_unauthorised()

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
