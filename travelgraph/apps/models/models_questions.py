import pdb
import json
from datetime import datetime

from travelgraph.apps.database import postgre, cursor
from travelgraph.apps.models import models_tags

def add_question(user_id, question_title, question_desc, question_tags):
    
    response = {}

    # All tags should be low case

    question_tags = question_tags.split(',')
    question_tags = [ str(tag.lower().strip()) for tag in question_tags ]

    question_text = unicode(question_text)
    question_desc = str(question_desc)
    user_id = str(user_id)

    created_ts = datetime.now()

    query = """ INSERT INTO "doobie_questions"
                (title, description, user_id, created_ts) 
                 VALUES ('{0}', '{1}', '{2}', '{3}') 
                 RETURNING question_id """.format(
                    question_text, question_desc,
                    user_id, created_ts)

    #pdb.set_trace()
    cursor.execute(query)

    postgre.commit()

    # Take question id and add tags to the main table and connect them

    question_id = cursor.fetchone()[0]

    # Add these tags to mapping table
    for tag in question_tags:
        models_tags.map_tag_to_doobie(tag, question_id, 'question')

    response.update({
        'status': 'success',
        'message': 'question successfully added',
        'question': question_text,
        'user_id': user_id,
    })

    return response

def get_question(question_id):
    '''
    General Function to get the question details of a given question_id
    '''

    response = {}

    query = """ SELECT * FROM "doobie_questions" 
                    WHERE question_id = '{0}' """.format(question_id)

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        response.update({
            'question_id': result['question_id'],
            'question_text': result['title'],
            'question_desc': result['description'],
            'asked_by_user_id': result['user_id']
        })

    return response

# Fix below function
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
        query = """ SELECT question_id FROM "tag_questions"
                    WHERE tag_id = '{0}' """.format(tag_id)

        cursor.execute(query)
        result = cursor.fetchall()

        if result:
            for row in result:
                question_list.append(row['question_id'])

    # We do not want duplicates, do we!
    question_list = list(set(question_list))

    for question_id in question_list:
        # Taking all the question data
        response['question'].append(get_question(question_id))

    response.update({
        'status':'success',
        'message':'{0} question(s) found'.format(len(response['questions'])),
    })

    return response

def view_all_questions():
    '''
    Get all the questions
    '''

    question_list = []

    response = {}

    response['questions'] = []

    query = """ SELECT * FROM "doobie_questions" """

    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for question in result:
            response['questions'].append({
                'question_id': question['question_id'],
                'question_text': question['title'],
                'question_desc': question['description'],
                'asked_by_user_id': question['user_id']
            })

    response.update({
        'status':'success',
        'message':'{0} question(s) found'.format(len(response['questions'])),
    })

    return response


def get_user_questions(user_id):
    '''
    Get all the questions asked by a specific user
    '''

    response = {
        'questions': [],
    }
    
    query = """ SELECT * FROM "doobie_questions"
                WHERE user_id = '{0}' """.format(user_id)

    cursor.execute(query)

    result = cursor.fetchall()

    if result:
        for question in result:
            response['questions'].append({
                'question_id': question['question_id'],
                'question_text': question['title'],
                'question_desc': question['description'],
                'asked_by_user_id': question['user_id']
            })

    response.update({
        'status':'success',
        'message':'{0} question(s) found'.format(len(response['questions'])),
    })

    return response


def subscribe_question(question_id, user_id):
    '''
    User wants to subscribe a question
    '''

    response = {}

    created_ts = datetime.now()

    doobie_id = get_doobie_id_question(question_id)

    query = """ INSERT INTO "user_doobie_follows"
                (user_id, doobie_id, created_ts)
                VALUES ('{0}', '{1}', '{2}') """.format(user_id,
                                            doobie_id, created_ts)

    cursor.execute(query)
    postgre.commit()

    response.update({
        'status': 'success',
        'message': 'user_id - {0} subscribed to question_id - {1} '.format(
                                                        question_id, user_id)
    })

    return response


def map_to_doobie(question_id, user_id):

    doobie_type_id = get_doobie_type_id('question')
    
    query = """ INSERT INTO "doobie" (type, mapping_id)
                VALUES ('{0}', '{1}') """.format(doobie_type_id, question_id)

    cursor.execute(query)
    postgre.commit()


def get_doobie_type_id(doobie_type):

    query = """ SELECT * FROM "doobie_type"
                WHERE name = '{0}' """.format(doobie_type)

    cursor.execute(query)
    doobie_type_id = cursor.fetchone()['id']

    return doobie_type_id


def get_doobie_id_question(question_id):

    doobie_type_id = get_doobie_type_id('question')

    query = """ SELECT * FROM "doobie"
                WHERE type = '{0}' AND
                      mapping_id = '{1}' """.format(
                                    doobie_type_id, question_id)

    cursor.execute(query)

    doobie_id = cursor.fetchone()['doobie_id']

    return doobie_id
