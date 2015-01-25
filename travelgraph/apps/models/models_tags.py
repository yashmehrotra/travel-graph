import pdb
import json

from travelgraph import settings
from travelgraph.apps.database import postgre, cursor


def get_tag_id(tag):
    '''
    Retrieves tag_id of a given tag
    '''
    
    query = """ SELECT tag_id FROM "tags" 
        WHERE tag_value = '{0}' """.format(
        tag)

    cursor.execute(query)

    result = cursor.fetchone()

    #pdb.set_trace()

    # No tag exists
    if not result:
        # Creating an empty list 
        question_list = json.dumps([])

        query = """ INSERT INTO "tags" (tag_value, question_list) VALUES ('{0}', '{1}') RETURNING tag_id""".format(
            tag, question_list)

        cursor.execute(query)
        postgre.commit()

        tag_id = cursor.fetchone()[0]
        return tag_id

    else:
        tag_id = result['tag_id']
        return tag_id


def add_question_to_tag(tag, ques_id):
    
    tag_id = get_tag_id(tag)

    query = """ SELECT question_list FROM "tags" WHERE tag_id = '{0}' """.format(tag_id)

    cursor.execute(query)
    result = cursor.fetchone()

    question_list = json.loads(result['question_list'])

    question_list.append(ques_id)
    question_list = json.dumps(question_list)

    query = """ UPDATE "tags" SET question_list = '{0}' WHERE tag_id = '{1}' """.format(question_list, tag_id)

    cursor.execute(query)
    postgre.commit()