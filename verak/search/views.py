from flask import Blueprint, request

api_search = Blueprint('api_search', __name__)


@api_search.route('/<query>', methods=['GET'])
def search_view(query):
    """
    Used for basic searching of questions
    and answers through elasticsearch
    """
    pass
