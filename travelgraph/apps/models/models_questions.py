import pdb
import json

from travelgraph.apps.database import postgre, cursor
from travelgraph.apps.models import models_tags

def add_question(user_id, api_key,
    question_text, question_desc, question_tags):
    
    response = {}

    # All tags should be low case

    question_tags = question_tags.split(',')
    question_tags = [ str(tag.lower().strip()) for tag in question_tags ]

    question_text = str(question_text)
    question_desc = str(question_desc)
    user_id = str(user_id)

    query = """ INSERT INTO "questions" (question_text, question_desc, question_tags, user_id) 
                 VALUES ('{0}', '{1}', '{2}', '{3}') 
                 RETURNING question_id """.format(
                    question_text, question_desc, json.dumps(question_tags), user_id)

    #pdb.set_trace()
    cursor.execute(query)

    postgre.commit()

    # Take question id and add tags to the main table and connect them

    question_id = cursor.fetchone()[0]

    for tag in question_tags:
        models_tags.add_question_to_tag(tag, question_id)

    response.update({
        'status':'success',
        'message':'question successfully added',
        'question':question_text,
    })

    return response


def view_tagged_questions(tags):
    '''
    Get all the questions related to the given tag(s)
    '''

    question_list = []

    response = {}

    response['questions'] = []

    #pdb.set_trace()

    # Always better to work with a list of tags
    if type(tags) == str or type(tags) == unicode:
        tags = [str(tags)]

    tag_ids = [ models_tags.get_tag_id(str(tag)) for tag in tags ]

    for tag_id in tag_ids:
        # Compiling a list of all the questions related to the tag
        query = """ SELECT question_list FROM "tags"
                    WHERE tag_id = '{0}' """.format(tag_id)

        cursor.execute(query)
        result = cursor.fetchone()

        question_list += json.loads(result['question_list'])

    # We do not want duplicates, do we!
    question_list = list(set(question_list))

    for question_id in question_list:
        # Taking all the question data
        query = """ SELECT * FROM "questions" 
                    WHERE question_id = '{0}' """.format(question_id)

        cursor.execute(query)
        result = cursor.fetchone()

        if result:

            response['questions'].append({
                'question_id':result['question_id'],
                'question_text':result['question_text'],
                'question_desc':result['question_desc'],
                'question_tags':result['question_tags'],
                'asked_by_user_id':result['user_id']
            })

    response.update({
        'status':'success',
        'message':'{0} question(s) found'.format(len(response['questions'])),
    })

    return response

def view_all_questions():
    pass
    