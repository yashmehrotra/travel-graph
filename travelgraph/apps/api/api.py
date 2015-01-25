from flask import request, session
import hashlib
import json
import pdb

from travelgraph import app, settings
from travelgraph.apps import auth

from travelgraph.apps.models import models, models_questions 
from travelgraph.apps import user_session


@app.route('/api/signup', methods=['POST'])
def api_signup():
    '''
    Recieves a POST request to create the user
    '''

    email      = request.form.get('email')
    password   = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name  = request.form.get('last_name')
    method     = request.form.get('method')

    result = models.create_user(email=email, method=method,
        first_name=first_name, last_name=last_name,  password=password)

    return 'User created - {0}'.format(result)


@app.route('/api/login', methods=['POST'])
def api_login():
    '''
    It takes email and password and logs in the user
    '''
    
    email    = request.form.get('email')
    password = request.form.get('password')

    response = models.auth_user(email=email, method='normal', password=password)
    if response['status'] == 'success':
        user_session.create_session(email)

    return json.dumps(response)


@app.route('/api/users', methods=['GET'])
def api_users():
    '''
    This is to see a list of all the users, meant for dev purposes
    '''

    x = ''
    for user in users:
        x += 'user - ' + user.email
        x += '\n'
        x += 'pass - ' + user.password
        x += '\n'

    return x


@app.route('/api/content/add_question', methods=['POST'])
def api_add_question():
    '''
    The question details should be added
    '''
    question      = request.form.get('question_text')
    question_desc = request.form.get('question_desc')
    question_tags = request.form.get('question_tags')

    # Take user id and api key from session
    api_key = session.get('api_key','xyzdd')
    user_id = session.get('user_id','15')

    #pdb.set_trace()

    result = models_questions.add_question(user_id, api_key,
        question, question_desc, question_tags)

    return result['status'] + ' ' + str(user_id)


@app.route('/api/content/view_tag/<tag>', methods=['GET'])
def view_tagged_ques(tag):
    '''
    Display a list of all the questions related to the tag given
    '''
    if '-' in tag:
        tag = tag.split('-')
    result = models_questions.view_tagged_questions(tag)

    return json.dumps(result)