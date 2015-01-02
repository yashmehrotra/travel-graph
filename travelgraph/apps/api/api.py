from travelgraph import app
from flask import request


@app.route('/api/signup', methods=['POST'])
def api_signup():
    return "YAHOO"
