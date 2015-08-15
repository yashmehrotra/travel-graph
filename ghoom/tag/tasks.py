from ghoom.models import (
    DbTag,
    DbDoobieTagMapping,
    session
)

from ghoom.tag.utils import (
    get_tag_id
)


def add_tags_to_doobie(tags, doobie):
    """
    Maps tags to doobies
    """

    if type(tags) != list:
        tags = [tags]

    tag_mapping = []
    for tag in tags:

        tag_id = get_tag_id(tags)
        doobie_id = doobie.doobie.id

        tag_mapping.append(
            DbDoobieTagMapping(doobie_id=doobie_id,
                               tag_id=tag_id,
                               tag_name=tag)
        )

    session.add(tag_mapping)
    session.commit()

    return None
