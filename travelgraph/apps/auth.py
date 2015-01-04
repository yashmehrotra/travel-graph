import hashlib
from py2neo import Graph, Node

from travelgraph import settings

graph = Graph(settings.graph_uri)


def create_user(email, password):
    
    password = hashlib.md5(password).hexdigest()
    
    user = Node(
        'user',
        email=email,
        password=password,
    )
    
    node_created = graph.create(user)
    node_value = str(node_created[0].ref)

    return node_value


def create_session(email):
    # Add session here
    print 'sss'
    pass
