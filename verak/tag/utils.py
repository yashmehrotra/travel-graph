from verak.models import (
    DbDoobieTagMapping,
    DbTag,
    session
)


def get_tag_id(tag):
    """
    Get tag_id by tag name
    If tag doesn't exist, create a new one
    """

    tag = tag.lower()

    tag_obj = session.query(DbTag).\
                filter(DbTag.name == tag).\
                first()

    if not tag_obj:
        new_tag = DbTag(name=tag)
        session.add(new_tag)
        session.commit()
        return new_tag.id

    return tag_obj.id


def get_doobies_from_tag(tag, serialized=False, doobie_type=None):
    """
    Returns a list of doobies attached to a tag
    If serialized is True, doobies will be returned
    in serialized form
    """

    if type(tag) != int:
        tag = get_tag_id(tag)

    doobies = session.query(DbDoobieTagMapping).\
                filter(DbDoobieTagMapping.tag_id == tag)

    if doobie_type:
        # TODO: Choose either Questions, answers of blogs
        pass

    doobies = doobies.all()

    data = []

    for doobie in doobies:
        if not serialized:
            data.append(doobie.doobie_id)
        else:
            # Serialized here
            pass

    return data
