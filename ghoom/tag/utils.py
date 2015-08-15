from ghoom.models import (
    DbTag,
    session
)


# How about bulk
# reading of the tags
def get_tag_id(tag):
    """
    Get tag_id by tag name
    """

    tag = session.query(DbTag).\
            filter(DbTag.name == tag).\
            first()

    return tag.id
