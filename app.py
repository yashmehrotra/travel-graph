from flask import Flask, render_template
from settings import *
from py2neo import Graph, Node, Relationship
import pdb

app = Flask(__name__)

graph = Graph(graph_uri)


@app.route('/')
def hello():
    return render_template('login.html')


@app.route('/medium')
def editor():
    return render_template('med.html')


@app.route('/graph')
def graph_db():
	pdb.set_trace()
	yash = Node('wanderer', name='Yash',age=19)
	wayne = Node('wanderer', name='Wayne',age=29)

	y_k_w = Relationship(yash,'KNOWS',wayne)
	graph.create(y_k_w)

	return 'Hello World'


if __name__ == '__main__':
    app.run()