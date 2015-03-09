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
    def get_doobie_ie(doobie_type, mapping_id):
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