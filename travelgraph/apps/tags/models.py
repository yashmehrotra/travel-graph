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

class Tags(Base):
    '''
    The tags table
    '''

    __tablename__ = "Tags"

    tag_id = Column(BigInteger, autoincrement=True, primary_key=True)
    type   = Column(UnicodeText())
    tag    = Column(UnicodeText())


    def get_tag_id(self, tag):
        '''
        Retrieves tag_id of a given tag.
        If no tag exists then a new tag is creaed.
        '''

        query_tag = session.query(Tags).filter_by(tag=tag).first()

        if not query_tag:
            new_tag = Tags(type='', tag=tag)
            session.add(new_tag)
            session.commit()

            return new_tag.tag_id

        else:
            return query_tag.tag_id


    def get_tag(self, tag_id):
        '''
        Get all the tag details corresponding to the given tag_id.
        '''

        tag = session.query(Tags).filter_by(tag_id=tag_id).first()

        response.update({
            'tag_id': tag.tag_id,
            'type': tag.type,
            'tag': tag.tag,
        })

        return response


# Below is for the stupid testing
pdb.set_trace()
x = Tags().get_tag_id(u'yash')



