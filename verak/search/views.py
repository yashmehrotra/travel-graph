from flask import Blueprint, request
from flask_restful import Api, Resource

search_blueprint = Blueprint('api_search', __name__)
api_search = Api(search_blueprint)


class ApiSearchView(Resource):
    """
    Used for basic searching of questions
    and answers through elasticsearch
    """

    url_endpoint = '/'
    api_blueprint = api_search

    def get(self):
        """
        Get Handler
        """

        query = request.args.get('q')
        return query
