import pdb
import json
from datetime import datetime

from travelgraph.apps.database import postgre, cursor
from travelgraph.apps.models import models_tags


def add_answer(question_id, answer_text, answer_tags,user_id):
    '''
    Storing answer for a given question
    '''

    response = {}

    answer_tags = answer_tags.split(',')
    answer_tags = [ str(tag.lower().strip()) for tag in answer_tags ]

    created_ts = datetime.now()

    query = """ INSERT INTO "doobie_answers"
                (answer, question_id, user_id, created_ts) 
                VALUES ('{0}', '{1}', '{2}', '{3}')
                    RETURNING answer_id """.format(answer_text,
                                question_id, user_id, created_ts)

    cursor.execute(query)
    postgre.commit()

    answer_id = cursor.fetchone()[0]

    # Add tags to the mapping table
    for tag in answer_tags:
        models_tags.map_tag_to_doobie(tag, answer_id, 'answer')

    map_to_doobie(answer_id, user_id)

    response.update({
        'status': 'success',
        'message': 'Answer added successfully'
    })

    return response


def get_answer(answer_id):
    '''
    Retrieving the details of a single answer
    '''

    response = {}

    query = """ SELECT * FROM "doobie_answers"
                WHERE answer_id = '{0}' """.format(answer_id)

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        response.update({
            'answer_id': result['answer_id'],
            'answer': result['answer'],
            # 'answer_tags': json.loads(result['answer_tags']),
            'question_id': result['question_id'],
            'user_details': user_details(result['user_id']),
        })

    return response

def get_all_answers(question_id):
    '''
    Retrieving all the answers for a specific question
    '''

    response = {
        'answers': [],
    }

    query = """ SELECT answer_id FROM "doobie_answers" 
                WHERE question_id = '{0}' """.format(question_id)

    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        for row in result:
            response['answers'].append(get_answer(row['answer_id']))

    response.update({
        'status': 'success',
        'message': '{0} answer(s) found'.format(len(response['answers'])),
        'question_id' : '{0}'.format(question_id)
    })

    return response


def get_user_answer(user_id, question_id=None):
    '''
    Get either all of the user's answers or Get his answer for a specific question
    '''

    response = {}

    if not question_id:
        '''
        We Want all of the user's answers
        '''

        response['answers'] = []
        query = """ SELECT * FROM "doobie_answers"
                    WHERE user_id = '{0}' """.format(user_id)

        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            for row in result:
                response['answers'].append({
                    'answer_id': row['answer_id'],
                    'answer': row['answer'],
                    #'answer_tags': json.loads(row['answer_tags']),
                    'question_id': row['question_id'],
                    'user_id': row['user_id'],
                })

            response.update({
                'status': 'success',
                'message': '{0} answer(s) found'.format(len(response['answers'])),
            })

        return response

    else:
        '''
        We want a user's answer for a specific question
        '''

        response['answers'] = {}

        query = """ SELECT * FROM "doobie_answers"
                    WHERE user_id = '{0}' AND
                    question_id = '{1}' """.format(user_id, question_id)

        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            response['answers'].update({
                'answer_id': result['answer_id'],
                'answer': result['answer'],
                #'answer_tags': json.loads(row['answer_tags']),
                'question_id': result['question_id'],
                'user_id': result['user_id']
            })

            response.update({
                'status': 'success',
            })

        return response


def user_details(user_id):
    '''
    Get some details about the asker of a question
    '''

    user_details = {}

    query = """ SELECT * FROM "user"
                WHERE user_id = '{0}' """.format(user_id)

    cursor.execute(query)
    user_data = cursor.fetchone()

    user_details.update({
        'status': 'success',
        'user_id': user_data['user_id'],
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'username': user_data['username'],
    })

    return user_details


def map_to_doobie(answer_id, user_id):

    doobie_type_id = get_doobie_type_id('answer')
    
    query = """ INSERT INTO "doobie" (type, mapping_id)
                VALUES ('{0}', '{1}') """.format(doobie_type_id, answer_id)

    cursor.execute(query)
    postgre.commit()


def get_doobie_type_id(doobie_type):

    query = """ SELECT * FROM "doobie_type"
                WHERE name = '{0}' """.format(doobie_type)

    cursor.execute(query)
    doobie_type_id = cursor.fetchone()['id']

    return doobie_type_id
