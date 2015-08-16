from ghoom.models import (
    DbTag,
    session
)


def get_tag_id(tag):
    """
    Get tag_id by tag name
    If tag doesn't exist, create a new one
    """

    tag = tag.lower()

    tag = session.query(DbTag).\
            filter(DbTag.name == tag).\
            first()

    if not tag:
        new_tag = DbTag(name=tag)

        session.add(new_tag)
        session.commit()
        return new_tag.id

    return tag.id
