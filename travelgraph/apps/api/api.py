from flask import request, session, jsonify
import hashlib
import json
import pdb

from travelgraph import app, settings
from travelgraph.apps import auth

from travelgraph.apps.models import models, models_questions, models_tags
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

    # Take user id and api key from form first then session
    user_id = request.form.get('user_id', session.get('user_id'))
    api_key = request.form.get('api_key', session.get('api_key'))

    #pdb.set_trace()

    result = models_questions.add_question(user_id, api_key,
        question, question_desc, question_tags)

    return jsonify(result)


@app.route('/api/content/view_tag/<tag>', methods=['GET'])
def view_tagged_ques(tag):
    '''
    Display a list of all the questions related to the tag given
    '''
    if '-' in tag:
        tag = tag.split('-')
    result = models_questions.view_tagged_questions(tag)

    return jsonify(result)


@app.route('/api/content/view_all_ques', methods=['GET'])
def view_all_ques():
    '''
    Display a list of all the questions
    '''

    result = models_questions.view_all_questions()

    return jsonify(result)


@app.route('/api/tag/subscribe_tag', methods=['POST'])
def subscribe_tag():
    '''
    User wants to subscribe to a tag
    '''

    user_id = request.form.get('user_id', session.get('user_id'))
    api_key = request.form.get('api_key', session.get('api_key'))
    tag     = request.form.get('tag')

    tag_id = models_tags.get_tag_id(tag)

    result = models_tags.user_subscribes_tag(user_id, api_key, tag_id)

    return jsonify(result)


@app.route('/api/user/follow_user', methods=['POST'])
def follow_user():
    '''
    User wants to follow another user
    '''

    user_id = request.form.get('user_id', session.get('user_id'))
    api_key = request.form.get('api_key', session.get('api_key'))

    user_id_to_follow = request.form.get('user_id_to_follow')

    result = models.user_follows_user(user_id, api_key, user_id_to_follow)

    return jsonify(result)
