from flask import jsonify
import redis

from settings import (
    REDIS_HOST,
    REDIS_PORT
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
