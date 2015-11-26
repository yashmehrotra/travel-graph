from flask import Blueprint, request
from flask_restful import Api, Resource
from elasticsearch import Elasticsearch

from verak.decorators import (
    auth_required,
    login_required
)

from verak.helpers import (
    response_json,
    response_error
)

from verak.settings import (
    ES_ADDRESS,
    ES_INDEX,
    ES_DOC_TYPE_DOOBIE
)

search_blueprint = Blueprint('api_search', __name__)
api_search = Api(search_blueprint)


class ApiSearchView(Resource):
    """
    Used for basic searching of questions
    and answers through elasticsearch
    """

    url_endpoint = '/search/'
    api_blueprint = api_search
    my_bp = search_blueprint
    my_api = Api(search_blueprint)
    auth = True

    def get(self):
        """
        Get Handler
        """

        es = Elasticsearch(ES_ADDRESS)
        # Use "title^2" for extra emphasis
        # TODO: Add this to a settings file
        #       or something global
        FIELDS = ["title", "description", "answer"]

        query = request.args.get('q')

        if not query:
            return response_error("No query provided")

        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": FIELDS,
                    "fuzziness": "AUTO"
                }
            }
        }
        search_result = es.search(index=ES_INDEX,
                                  doc_type=ES_DOC_TYPE_DOOBIE,
                                  body=body)

        return query
