from flask import jsonify
import redis
import hashlib
import random

from settings import (
    AUTH_KEY_NAMESPACE,
    ACCESS_TOKEN_NAMESPACE,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_AUTH_KEY_DB
)


def response_json(data={}, status=200):
    """
    Helper function to return
    json responses
    """

    response = jsonify(**data)
    response.status_code = status

    return response


def redis_client():

    redis_cli = redis.StrictRedis(host=REDIS_HOST,
                                  port=REDIS_PORT,
                                  db=REDIS_AUTH_KEY_DB)
    return redis_cli


def generate_key():
    """
    Used to generate auth_key and access_tokens
    """
    key = hashlib.sha256(str(random.getrandbits(256))).hexdigest()
    return key


def generate_auth_key(ttl):
    """
    Sets auth_key in redis
    """

    redis_cli = redis_client()
    auth_key = generate_key()

    value = json.dumps({'ttl': ttl})
    key = AUTH_KEY_NAMESPACE + auth_key

    redis_cli.set(key, ttl, value)

    return auth_key


def verify_auth_key(auth_key):
    """
    Verify user's auth_key
    """

    redis_cli = redis_client()
    auth_key = redis_cli.get(AUTH_KEY_NAMESPACE + auth_key)

    if not auth_key:
        return False

    return True
