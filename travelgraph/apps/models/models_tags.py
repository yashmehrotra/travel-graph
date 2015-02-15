import pdb
import json
from datetime import datetime

from travelgraph import settings
from travelgraph.apps.database import postgre, cursor


def get_tag_id(tag):
    '''
    Retrieves tag_id of a given tag, if no tag exists then a new tag is creaed
    '''
    
    query = """ SELECT tag_id FROM "tags" 
        WHERE name = '{0}' """.format(
        tag)

    cursor.execute(query)

    result = cursor.fetchone()

    # No tag exists
    if not result:
        query = """ INSERT INTO "tags" (name) 
                    VALUES ('{0}') RETURNING tag_id""".format(tag)

        cursor.execute(query)
        postgre.commit()

        tag_id = cursor.fetchone()[0]
        return tag_id

    else:
        tag_id = result['tag_id']
        return tag_id


def map_tag_to_doobie(tag, mapping_id, doobie_type):
    
    tag_id = get_tag_id(tag)

    doobie_type_id = get_doobie_type_id(doobie_type)

    query = """ INSERT INTO "doobie_tags_mapping"
                (tag_id, doobie_type, mapping_id) 
                VALUES ('{0}', '{1}', '{2}') 
                RETURNING id """.format(
                        tag_id, doobie_type_id, mapping_id)

    cursor.execute(query)
    postgre.commit()


def user_subscribes_tag(user_id, tag_id):
    '''
    When a user subscribes to a tag
    '''
    
    response = {}

    created_ts = datetime.now()

    query = """ INSERT INTO "user_tags_follows" (user_id, tag_id, created_ts) 
                VALUES ('{0}', '{1}', '{2}') """.format(user_id,
                                                tag_id, created_ts)

    cursor.execute(query)
    postgre.commit()

    response.update({
        'status':'success',
        'message':'Tag successfully subscribed',
    })

    return response


def get_tag(tag_id):
    '''
    Get tag value corresponding to a tag_id
    '''

    response = {}

    query = """ SELECT * FROM "tags"
                WHERE tag_id = '{0}' """.format(tag_id)

    cursor.execute(query)

    result = cursor.fetchone()

    response.update({
        'tag_id': result['tag_id'],
        'tag_value': result['name']
    })

    return response


def get_user_tags(user_id):
    '''
    Retrieve all the tag_ids and tags followed by a user
    '''

    # Format of response['tags'] = [ {tag_id,tag}, {tag_id,tag}, {tag_id,tag},... ]

    response = {
        'user_id': user_id,
        'tags': [],
    }

    query = """ SELECT * FROM "user_tags_follows"
                WHERE user_id = '{0}' """.format(user_id)

    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        response['tags'] = [ get_tag(tag['tag_id']) for tag in result ]

    response.update({
        'status': 'success',
        'message': '{0} tag(s) found'.format(len(response['tags']))
    })

    return response


def get_doobie_type_id(doobie_type):

    query = """ SELECT * FROM "doobie_type"
                WHERE name = '{0}' """.format(doobie_type)

    cursor.execute(query)
    doobie_type_id = cursor.fetchone()['id']

    return doobie_type_id


def get_tags_for_doobie(doobie_type, mapping_id):
    '''
    Get all the tags for a specific doobie
    '''

    tags = []

    query = """ SELECT * FROM "doobie_tags_mapping"
                WHERE doobie_type = '{0}' AND
                mapping_id = '{1}' """.format(doobie_type, mapping_id)

    cursor.execute(query)

    result = cursor.fetchall()

    for row in result:
        tags.append(get_tag(row['tag_id']))

    return tags