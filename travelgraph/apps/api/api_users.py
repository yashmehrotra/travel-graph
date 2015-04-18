from flask import request, session, jsonify
import hashlib
import json
import pdb

from travelgraph import app, settings
from travelgraph.apps import auth

from travelgraph.apps.models import (
        models,
        models_questions,
        models_tags,
        models_answers
    )

from travelgraph.apps import user_session


@app.route('/api/signup', methods=['POST'])
def api_signup():
    '''
    Recieves a POST request to create the user
    '''

    email         = request.form.get('email')
    password      = request.form.get('password', '')
    first_name    = request.form.get('first_name')
    last_name     = request.form.get('last_name')
    profile_photo = request.form.get('profile_photo','')
    method        = request.form.get('method')

    result = models.create_user(
        email=email, method=method,
        first_name=first_name, last_name=last_name,
        profile_photo=profile_photo, password=password)

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

    return jsonify(response)


@app.route('/api/logout')
def api_logout():
    '''
    Destroys the session and logs user out
    '''

    user_session.destroy_session()

    response = {
        'status': 'success',
        'message': 'user logged out'
    }

    return jsonify(response)


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


@app.route('/api/user/<user_id>/')
def api_user(user_id):
    '''
    Stuff
    '''

    result = models.user_profile(user_id)

    return jsonify(result)
