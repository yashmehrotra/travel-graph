from flask import jsonify
import redis
import mandrill

from settings import (
    MANDRILL_API_KEY,
    REDIS_HOST,
    REDIS_PORT,
    WEBSITE_URL
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


def send_mail(from_email=None, to_email=None, subject=None, body=None):
    """
    Generic Function for sending emails
    """

    mandrill_cli = mandrill.Mandrill(MANDRILL_API_KEY)

    message = {
        'from_email': from_email,
        'headers': {'Reply-To': from_email},
        'html': body,
        'metadata': {'website': WEBSITE_URL},
        'subject': subject,
        'to': to_email
    }

    mandrill_cli.messages.send(message=message, async=True)
