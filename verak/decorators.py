from flask import request
# TODO: Decide whether encryption has to be used
# import urllib
# import base64

from verak.helpers import response_unauthorised
from verak.user.utils import (
    verify_auth_key,
    verify_access_token
)


def auth_required(f):
    """
    Checks user's auth_key
    """
    def wrap(*args, **kwargs):
        auth_key = request.headers.get('Authkey')
        if not auth_key:
            return response_unauthorised()

        # For encoded keys
        # if len(auth_key) != 64:
        #    auth_key = base64.b64decode(urllib.unquote(auth_key))
        #    request.headers['auth_key'] = auth_key

        verify_auth_key(auth_key)

        return f(*args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def login_required(f):
    """
    Check whether the access token exists
    """

    def wrap(*args, **kwargs):

        access_token = request.headers.get('Accesstoken')

        if not access_token:
            return response_unauthorised()

        acc_tok_obj = verify_access_token(access_token)

        if not acc_tok_obj:
            return response_unauthorised()

        user_id = acc_tok_obj['user_id']
        request.user_id = int(user_id)

        return f(*args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
