import json
from datetime import datetime
import pdb

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from sqlalchemy import event
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import select

from sqlalchemy import create_engine

from travelgraph.apps.doobies.models import DoobieType
from travelgraph.apps.doobies.models import Doobie
# Make sure this doesn't cause a problem in the future
from travelgraph.apps.tags.models import DoobieTagsMapping
from travelgraph.apps.tags.models import Tags

SQLALCHEMY_ENGINE = 'postgresql://yash:44rrff@localhost:5432/'
DATABASE = 'G2'

Base = declarative_base()
engine = create_engine(SQLALCHEMY_ENGINE+DATABASE)
Session = sessionmaker(bind=engine)

session = Session()

class Answers(Base):
    '''
    The main Answers Doobie
    '''

    __tablename__ = "Answers"

    DOOBIE_NAME = "answers"

    anwser_id   = Column(BigInteger, autoincrement=True, primary_key=True)
    answer      = Column(UnicodeText())
    question_id = Column(BigInteger, primary_key=True)
    user_id     = Column(BigInteger, primary_key=True)
    created_ts  = Column(DateTime, default=datetime.now())
    updated_ts  = Column(DateTime, default=datetime.now())

    @staticmethod
    def add_answer(answer, question_id, user_id, tags=None):
        '''
        Adding a new answer
        :params
        - answer: unicode string
        - question_id: bigint
        - user_id: bigint
        - tags: list
        '''

        new_answer = Answers(answer=answer,
                             question_id=question_id,
                             user_id=user_id)

        session.add(new_answer)
        session.commit()

        answer_id = new_answer.anwser_id

        # It should return the id, make sure it does that
        doobie_type = DoobieType.get_doobie_type(DOOBIE_NAME)

        # Mapping answer to Doobie
        doobie_mapping = Doobie.map_doobie(doobie_type, answer_id)

        # The tags recieved here should be sanitized, or pass the list directly with doobie credentials and let tags app do the work hmm...
        if tags:
            pass

        response = {
            'anwser_id': new_answer.anwser_id,
            'answer': new_answer.answer,
            'question_id': new_answer.question_id,
            'user_id': new_answer.user_id,
            'doobie_id': doobie_mapping.doobie_id,
        }

        return response


    @staticmethod
    def get_answer(anwser_id):
        '''
        Get the whole answer details
        '''

        ##
        ## ADD TAG FUNCTIONALITY LATER
        ##

        answer = session.query(Answer).\
                    filter(Answer.answer_id == answer_id)

        answer_data = {
            'answer_id': answer.answer_id,
            'answer': answer.answer,
            'question_id': answer.question_id,
            'user_id': answer.user_id,
            'created_ts': answer.created_ts,
            'updated_ts': answer.updated_ts
        }

        return answer_data


    @staticmethod
    def get_answer_ids(question_id=None, user_id=None):
        '''
        Get answer ids for the above parameters
        '''

        if question_id and user_id:
            answer_ids = session.query(Answer.c.answer_id).\
                        filter(Answer.question_id == question_id,
                               Answer.user_id == user_id)

        elif question_id and not user_id:
            answer_ids = session.query(Answer.c.answer_id).\
                        filter(Answer.question_id == question_id)

        elif not question_id and user_id:
            answer_ids = session.query(Answer.c.answer_id).\
                        filter(Answer.user_id == user_id)

        elif not question_id and not user_id:
            answer_ids = None

        return answer_ids


