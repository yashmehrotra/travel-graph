from flask import request
from py2neo import Graph, Node
import hashlib
import json

from travelgraph import app, settings
from travelgraph.apps import auth

graph = Graph(settings.graph_uri)


@app.route('/api/signup', methods=['POST'])
def api_signup():
    email = request.form['email']
    password = request.form['password']

    node_value = auth.create_user(email, password)

    return 'User created at node val {0}'.format(node_value)


@app.route('/api/login', methods=['POST'])
def api_login():
    email = request.form['email']
    password = request.form['password']

    password = hashlib.md5(password).hexdigest()

    query = graph.find_one('user', property_key='email', property_value=email)
    if query and password == query.get_properties()['password']:
        auth.create_session(email)
        z = {'status':'success','message':'ses created'}
    else:
        z = 'wrong go away'
    return json.dumps(z)


@app.route('/api/users', methods=['GET'])
def api_users():

    users = graph.cypher.execute(
        "MATCH (u:user) RETURN u.email as email, u.password as password"
    )

    x = ''
    for user in users:
        x += 'user - ' + user.email
        x += '\n'
        x += 'pass - ' + user.password
        x += '\n'

    return x
