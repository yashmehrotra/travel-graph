from flask import request
from py2neo import Graph, Node

from travelgraph import app, settings

graph = Graph(settings.graph_uri)


@app.route('/api/signup', methods=['POST'])
def api_signup():
    email = request.form['email']
    # convert password to md5
    password = request.form['password']

    user = Node(
        'user',
        email=email,
        password=password,
    )
    graph.create(user)
    return 'success , do this in json'


@app.route('/api/login', methods=['POST'])
def api_login():
    email = request.form['email']
    password = request.form['password']

    query = graph.find_one('user', property_key='email', property_value=email)
    if query and password == query.get_properties()['password']:
        z = 'correct login that user'
    else:
        z = 'wrong go away'
    return z


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
