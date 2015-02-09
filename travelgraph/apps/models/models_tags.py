import pdb
import json

from travelgraph import settings
from travelgraph.apps.database import postgre, cursor


def get_tag_id(tag):
    '''
    Retrieves tag_id of a given tag, if no tag exists then a new tag is creaed
    '''
    
    query = """ SELECT tag_id FROM "tags" 
        WHERE tag_value = '{0}' """.format(
        tag)

    cursor.execute(query)

    result = cursor.fetchone()

    # No tag exists
    if not result:
        query = """ INSERT INTO "tags" (tag_value) 
                    VALUES ('{0}') RETURNING tag_id""".format(tag)

        cursor.execute(query)
        postgre.commit()

        tag_id = cursor.fetchone()[0]
        return tag_id

    else:
        tag_id = result['tag_id']
        return tag_id


def add_question_to_tag(tag, ques_id):
    
    tag_id = get_tag_id(tag)

    query = """ INSERT INTO "tag_questions" (tag_id, question_id) 
                    VALUES ('{0}', '{1}') """.format(
                                        tag_id, ques_id)

    cursor.execute(query)
    postgre.commit()


def user_subscribes_tag(user_id, api_key, tag_id):
    '''
    When a user subscribes to a tag
    '''
    
    response = {}

    query = """ INSERT INTO "tag_subscribers" (user_id, tag_id) 
                VALUES ('{0}', '{1}') """.format(user_id,tag_id)

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
        'tag_value': result['tag_value']
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

    query = """ SELECT * FROM "tag_subscribers"
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

