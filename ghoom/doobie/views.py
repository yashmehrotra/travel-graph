from flask import Blueprint, request

from ghoom.models import (
    DbAnswer,
    DbDoobieMapping,
    DbDoobieTagMapping,
    DbQuestion,
    DbTag,
    DbUser,
    session
)
from ghoom.decorators import (
    auth_required,
    login_required
)

from ghoom.helpers import (
    response_json,
    response_error
)

api_question = Blueprint('api_question', __name__)
api_answer = Blueprint('api_answer', __name__)


@api_question.route('/<question_id>', methods=['GET', 'POST', 'PUT'])
@auth_required
@login_required
def question_view(question_id=None):
    """
    Main question view
    """

    if request.method == 'GET':

        if not question_id:
            return response_error("question_id not provided")

        question = session.query(DbQuestion).\
                    get(question_id)
        # Below is temp
        return response_json(question.serialize)

    elif request.method == 'POST':

        try:
            title = request.form['title']
            description = request.form.get('description')
            tags = request.form.get('tags')
        except KeyError:
            response_error("missing parameters")

        question = DbQuestion(title=title,
                              description=description,
                              user_id=request.user_id)

        session.add(question)
        session.commit()
        # Below is temp
        return response_json(question.serialize)
