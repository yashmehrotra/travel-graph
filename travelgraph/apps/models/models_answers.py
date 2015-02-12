import pdb
import json

from travelgraph.apps.database import postgre, cursor


def add_answer(question_id, answer_text, user_id):
    '''
    Storing answer for a given question
    '''

    response = {}

    query = """ INSERT INTO "answers" (answer, question_id, user_id) 
                VALUES ('{0}', '{1}', '{2}') """.format(answer_text,
                                                question_id, user_id)

    cursor.execute(query)
    postgre.commit()

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

    query = """ SELECT * FROM "answers"
                WHERE answer_id = '{0}' """.format(answer_id)

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        response.update({
            'answer_id': result['answer_id'],
            'answer': result['answer'],
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

    query = """ SELECT answer_id FROM "answers" 
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
        query = """ SELECT * FROM "answers"
                    WHERE user_id = '{0}' """.format(user_id)

        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            for row in result:
                response['answers'].append({
                    'answer_id': row['answer_id'],
                    'answer': row['answer'],
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

        query = """ SELECT * FROM "answers"
                    WHERE user_id = '{0}' AND
                    question_id = '{1}' """.format(user_id, question_id)

        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            response['answers'].update({
                'answer_id': result['answer_id'],
                'answer': result['answer'],
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
        'username': user_data['name'],
    })

    return user_details
