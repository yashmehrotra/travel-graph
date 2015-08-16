from ghoom.models import (
    DbTag,
    DbDoobieTagMapping,
    session
)

from ghoom.tag.utils import (
    get_tag_id
)


def map_tags_to_doobie(tags, doobie_id):
    """
    Maps tags to doobies
    """

    if type(tags) != list:
        tags = [tags]

    tag_mapping = []
    for tag in tags:

        tag_id = get_tag_id(tag)

        tag_mapping.append(
            DbDoobieTagMapping(doobie_id=doobie_id,
                               tag_id=tag_id,
                               tag_name=tag)
        )

    session.add_all(tag_mapping)
    session.commit()

    return True
