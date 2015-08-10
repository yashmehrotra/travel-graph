from ghoom.helpers import (
    response_json,
    verify_auth_key,
    verify_access_token
)


def auth_required(f):
    """
    Checks user's auth_key
    """
    def wrap(request, *args, **kwargs):

        resp = {}
        auth_key = request.headers.get('auth_key')

        if not auth_key:
            resp.update({
                'status': 'failed',
                'error': 'not authorised'
            })

            return response_json(data=resp,
                                 status=405)

        verified = verify_auth_key(auth_key)

        if not verified:
            resp.update({
                'status': 'failed',
                'error': 'auth_key verification failed'
            })

            return response_json(data=resp,
                                 status=401)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def login_required(f):
    """
    Check whether the access token exists
    """

    def wrap(request, *args, **kwargs):

        resp = {}
        access_token = request.headers.get('access_token')

        if not access_token:
            resp.update({
                'status': 'failed',
                'error': 'not authorised'
            })

            return response_json(data=resp,
                                 status=401)

        verified, user_id = verify_access_token(access_token)

        if not (verified or user_id):
            resp.update({
                'status': 'failed',
                'error': 'access_token verification failed'
            })

            return response_json(data=resp,
                                 status=401)

        request.user_id = user_id

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
