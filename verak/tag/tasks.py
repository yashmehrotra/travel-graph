from verak.models import (
    DbDoobieTagMapping,
    session
)

from verak.tag.utils import (
    get_tag_id
)

from verak.helpers import multimap


def map_tags_to_doobie(tags, doobie_id):
    """
    Maps tags to doobies
    :param tags: list
    :param doobie_id: int
    """

    # TODO: Add this function as a method
    #       in DbQuestion and DbAnswer

    # TODO: When Editing a doobie, make sure old tags are
    #       removed and only new/existing ones are there

    if type(tags) != list:
        tags = [tags]

    # Cleaning tags
    tags = filter(None, tags)
    tags = multimap([unicode.strip, unicode.lower], tags)

    tag_mapping = []
    current_tags = []

    existing_tags = session.query(DbDoobieTagMapping).\
                        filter(DbDoobieTagMapping.doobie_id == doobie_id)

    existing_tags = [t.tag_id for t in existing_tags]

    for tag in tags:

        tag_id = get_tag_id(tag, create=True)
        current_tags.append(tag_id)

        if tag_id in existing_tags:
            continue

        tag_mapping.append(
            DbDoobieTagMapping(doobie_id=doobie_id,
                               tag_id=tag_id,
                               tag_name=tag)
        )

    session.add_all(tag_mapping)
    session.commit()

    # To disable old tags
    ids_to_disable = list(set(existing_tags) - set(current_tags))

    if ids_to_disable:
        disable_query = session.query(DbDoobieTagMapping).\
                            filter(DbDoobieTagMapping.tag_id.in_(ids_to_disable),
                                   DbDoobieTagMapping.doobie_id == doobie_id)

        if disable_query:
            disable_query = disable_query.update({DbDoobieTagMapping.enabled: False},
                                                  synchronize_session=False)

            session.commit()

    return True
