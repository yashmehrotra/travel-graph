from flask import render_template
from py2neo import Graph, Node, Relationship
import pdb

from travelgraph import app

from settings import graph_uri

graph = Graph(graph_uri)


@app.route('/')
def page_login():
    return render_template('login.html')


@app.route('/signup')
def page_signup():
    return render_template('signup.html')


@app.route('/medium')
def editor():
    return render_template('med.html')


@app.route('/graph')
def graph_db():
    pdb.set_trace()
    yash = Node('wanderer', name='Yash', age=19)
    wayne = Node('wanderer', name='Wayne', age=29)

    y_k_w = Relationship(yash, 'KNOWS', wayne)
    graph.create(y_k_w)

    return 'Hello World'
