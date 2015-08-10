from flask import jsonify
import redis
import hashlib
import random
import json

from ghoom.models import DbRequestKey
from settings import (
    AUTH_KEY_NAMESPACE,
    ACCESS_TOKEN_NAMESPACE,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_AUTH_KEY_DB,
    REDIS_ACCESS_TOKEN_DB
)


def response_json(data={}, status=200):
    """
    Helper function to return
    json responses
    """

    response = jsonify(**data)
    response.status_code = status

    return response


def response_unauthorised():
    """
    Returns a not authorised response
    """

    response = {
        'status': 'failed',
        'error': 'Not Authorised'
    }

    return response_json(data=response, status=401)


def redis_client(db=0):

    redis_cli = redis.StrictRedis(host=REDIS_HOST,
                                  port=REDIS_PORT,
                                  db=db)
    return redis_cli


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
        return response_json(data=resp,
                             status=404)

    ttl = request_key_obj.ttl
    value = json.dumps({'ttl': ttl})
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
    return key


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
