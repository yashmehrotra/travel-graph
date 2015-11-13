from flask import Blueprint, request

from verak.models import (
    DbTag,
    DbDoobieTagMapping,
    session
)
from verak.decorators import (
    auth_required,
    login_required
)

from verak.tag.utils import get_tag_id
from verak.helpers import response_json

api_tag = Blueprint('api_tag', __name__)


@api_tag.route('/', methods=['GET'])
@api_tag.route('/<tag>/', methods=['GET'])
@auth_required
@login_required
def tag_view(tag=None):
    """
    Returns doobies corresponding to tag
    """
    if tag:
        tag = tag.lower()

        tag_id = get_tag_id(tag)

        doobies = session.query(DbDoobieTagMapping).\
                    filter(DbDoobieTagMapping.tag_id == tag_id,
                           DbDoobieTagMapping.enabled == True).\
                    all()

        doobies = [d.doobie.serialize for d in doobies]

        response = {
            'status': 'success',
            'doobies': doobies
        }

        return response_json(response)

    else:
        tags = session.query(DbTag).all()

        tags = [t.serialize for t in tags]

        response = {
            'status': 'success',
            'tags': tags,
        }

        return response_json(response)
