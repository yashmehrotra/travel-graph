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

SQLALCHEMY_ENGINE = 'postgresql://yash:44rrff@localhost:5432/'
DATABASE = 'G2'

Base = declarative_base()
engine = create_engine(SQLALCHEMY_ENGINE+DATABASE)
Session = sessionmaker(bind=engine)

session = Session()

class Doobie(Base):
    '''
    For Mapping Different Types of doobies
    '''

    __tablename__ = "Doobies"

    doobie_id   = Column(BigInteger, autoincrement=True, primary_key=True)
    doobie_type = Column(BigInteger) # Add foreign key
    mapping_id  = Column(BigInteger)


    @staticmethod
    def map_doobie(doobie_type, mapping_id):
        pass


    @staticmethod
    def get_doobie_id(doobie_type, mapping_id):
        pass


class DoobieType(Base):
    '''
    For keeping a count of diffent types of Doobies
    '''

    __tablename__ = "Doobie_type"

    id        = Column(BigInteger, autoincrement=True, primary_key=True)
    name      = Column(UnicodeText())
    tablename = Column(UnicodeText())


    @staticmethod
    def add_doobie(doobie, tablename):
        '''
        Add a new doobie type
        '''

        pass


    @staticmethod
    def get_doobie_type(doobie_name):
        '''
        Get doobie type id through name
        '''

        doobie_type = session.query(DoobieType.c.id).\
                              filter(DoobieType.name == doobie_name).first()

        return doobie_type


class UserDoobieFollow(Base):
    '''
    When User Follows a Doobie
    '''

    __tablename__ = 'user_doobie_follow'

    id         = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id    = Column(BigInteger, primary_key=True)
    doobie_id  = Column(BigInteger, primary_key=True)
    created_ts = Column(DateTime, default=datetime.now())

    @staticmethod
    def add_follower(user_id, doobie_id):
        '''
        When a user wants to follow a doobie
        '''

        response = {}

        doobie_follow = UserDoobieFollow(user_id=user_id, doobie_id=doobie_id)

        session.add(doobie_follow)
        session.commit()

        response.update({
            'status': 'success',
            'message': 'add message'
        })

        return response


    @staticmethod
    def view_all_followed_doobies(user_id):
        '''
        Get all the doobie_ids a user follows
        '''

        followed_doobies = session.query(UserDoobieFollow.c.doobie_id).\
                           filter(UserDoobieFollow.user_id==user_id)

        return followed_doobies


    @staticmethod
    def view_all_doobie_followers(doobie_id):
        '''
        Get all the user_id's who follow the given doobie_id
        '''

        user_follows = session.query(UserDoobieFollow.c.user_id).\
                        filter(UserDoobieFollow.doobie_id==doobie_id)

        return user_follows
