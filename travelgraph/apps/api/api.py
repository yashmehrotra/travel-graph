from flask import request
import hashlib
import json

from travelgraph import app, settings
from travelgraph.apps import auth

from travelgraph.apps.models import models 

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

    result = models.create_user(email=email, method=method, first_name=first_name, last_name=last_name,  password=password)

    return 'User created - {0}'.format(result)


@app.route('/api/login', methods=['POST'])
def api_login():
    '''
    It takes email and password and logs in the user
    '''
    
    email = request.form['email']
    password = request.form['password']

    z = models.auth_user(email=email, method='normal', password=password)
    return json.dumps(z)


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
