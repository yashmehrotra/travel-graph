from flask import jsonify
import redis

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


def verify_auth_key(auth_key):
    """
    Verify user's auth_key
    """

    redis_cli = redis.StrictRedis(host=REDIS_HOST,
                                  port=REDIS_PORT,
                                  db=REDIS_AUTH_KEY_DB)

    x = redis_cli.get(AUTH_KEY_NAMESPACE + auth_key)
    return True

