from flask import Blueprint, request

from verak.models import (
    DbTag,
    DbDoobieTagMapping,
    DbUserTagFollowing,
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


@api_tag.route('/follow/', methods=['POST'])
@auth_required
@login_required
def follow_tag_view(tag):
    """
    When a user wants to follow a tag
    """

    try:
        tag = request.form['tag']
    except KeyError:
        return response_error('Missing Parameters')

    tag_id = get_tag_id(tag)
    user_id = request.user_id

    relation_exists = session.query(DbUserTagFollowing).\
                        filter(DbUserTagFollowing.user_id == user_id,
                               DbUserTagFollowing.tag_id == tag_id).\
                        first()

    if relation_exists:
        # User has en existing relationship with tag

        if relation_exists.enabled:
            # Return error as user already follows the tag
            return response_error("User already follows this tag")
        else:
            relation_exists.enabled = True
            session.add(relation_exists)
            session.commit()

    else:
        # Create a new relation

        new_relation = DbUserTagFollowing(user_id=user_id,
                                          tag_id=tag_id,
                                          tag_name=tag)

        session.add(new_relation)
        session.commit()

    response = {
        'status': 'success',
        'message': 'User {0} is now following {1}'.\
                        format(user_id, tag)
    }

    return response_json(response)


@api_tag.route('/unfollow/', methods=['POST'])
@auth_required
@login_required
def unfollow_tag_view(tag):
    """
    To unfollow a tag
    """

    try:
        tag = request.form['tag']
    except KeyError:
        return response_error('Missing Parameters')

    tag_id = get_tag_id(tag)
    user_id = request.user_id

    relation = session.query(DbUserTagFollowing).\
                filter(DbUserTagFollowing.user_id == user_id,
                       DbUserTagFollowing.tag_id == tag_id).\
                first()

    if not relation:
        return response_error('No relationship exists')

    if not relation.enabled:
        return response_error('Already unfollowed')

    # Set the enabled flag to false
    relation.enabled = False

    session.add(relation)
    session.commit()

    response = {
        'status': 'success',
        'message': 'User {0} unfollowed {1}'.\
                        format(user_id, tag)
    }

    return response_json(response)
