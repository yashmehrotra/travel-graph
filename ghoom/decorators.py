from ghoom.helpers import (
    response_json,
    verify_auth_key
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
                                 status=405)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
