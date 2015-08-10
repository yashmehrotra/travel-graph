from flask import jsonify
import redis
import hashlib
import random
import json

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


def generate_auth_key(ttl):
    """
    Sets auth_key in redis
    """

    redis_cli = redis_client(db=REDIS_AUTH_KEY_DB)
    auth_key = generate_key()

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
        return False

    return True


def generate_access_token(user_id, ttl):
    """
    Sets access_token in redis
    """

    redis_cli = redis_client(db=REDIS_ACCESS_TOKEN_DB)
    access_token = generate_key()

    value = {
        'user_id': user_id,
        'ttl': ttl
    }

    value = json.dumps(value)

    key = ACCESS_TOKEN_NAMESPACE + access_token

    redis_cli.setex(key, ttl, value)


def verify_access_token(access_token):
    """
    Verify user's access_token and also return user_id
    """

    verified = False
    user_id = None

    redis_cli = redis_client(db=REDIS_ACCESS_TOKEN_DB)
    access_token = redis_cli.get(ACCESS_TOKEN_NAMESPACE + access_token)

    if not access_token:
        return verified, user_id

    user_id = json.loads(access_token)['user_id']
    verified = True

    return verified, user_id
