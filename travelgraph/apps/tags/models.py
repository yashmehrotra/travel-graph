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
    type   = Column(BigInteger) # Add foreign key
    tag    = Column(UnicodeText())


    @staticmethod
    def get_tag_id(tag):
        '''
        Retrieves tag_id of a given tag.
        If no tag exists then a new tag is creaed.
        '''

        query_tag = session.query(Tags).filter_by(tag=tag).first()

        if not query_tag:
            # The tag we searched for doesn't exist
            # Hence we create a new tag
            
            new_tag = Tags(type='', tag=tag)
            session.add(new_tag)
            session.commit()

            return new_tag.tag_id

        else:
            return query_tag.tag_id


    @staticmethod
    def get_tag(tag_id):
        '''
        Get all the tag details corresponding to the given tag_id.
        '''

        response = {}

        tag = session.query(Tags).filter_by(tag_id=tag_id).first()

        response.update({
            'tag_id': tag.tag_id,
            'type': tag.type,
            'tag': tag.tag,
        })

        return response


class TagType(Base):
    '''
    The tag_type table
    '''

    __tablename__ = "tag_type"

    id   = Column(BigInteger, autoincrement=True, primary_key=True)
    type = Column(UnicodeText())


class DoobieTagsMapping(Base):
    '''
    The Doobie_tags_mapping table
    '''

    __tablename__ = "Doobie_tags_mapping"

    id          = Column(BigInteger, autoincrement=True, primary_key=True)
    doobie_type = Column(BigInteger)
    mapping_id  = Column(BigInteger)
    tag_id      = Column(BigInteger) # Add appropriate foreign keys


    @staticmethod
    def map_tag_to_doobie(tag, doobie_type, mapping_id):
        '''
        Map tag to doobie - provide better desc here
        '''

        response = {}

        tag_id = Tags.get_tag_id(tag)
        
        new_mapping = DoobieTagsMapping(doobie_type=doobie_type,
                                        mapping_id=mapping_id,
                                        tag_id=tag_id)

        session.add(new_mapping)
        session.commit()

        response.update({
            'status': 'success'
        })

        return response


    @staticmethod
    def get_doobie_tags(doobie_type, mapping_id):
        '''
        Get all tags for a specific doobie
        '''

        tags = []

        query = session.query(DoobieTagsMapping).\
                        filter(DoobieTagsMapping.doobie_type == doobie_type,
                               DoobieTagsMapping.mapping_id == mapping_id)

        tag_ids = [ row.tag_id for row in query ]

        for tag_id in tag_ids:
            tags.append(Tags.get_tag(tag_id))

        return tags


    @staticmethod
    def get_tagged_doobies(**params):
        '''
        Get all the doobies related to a tag
        also add which parameters should be passed
        '''

        response = {}

        # Either tag or tag_id should be in the params, raise error if not

        tag_id = params.get('tag_id', Tags.get_tag_id(params.get('tag')))

        query = session.query(DoobieTagsMapping).\
                        filter(DoobieTagsMapping.tag_id == tag_id)

        if params.get('doobie_type'):
            query = query.filter(
                    DoobieTagsMapping.doobie_type == params['doobie_type'])

        doobies = []

        for row in query:
            doobies.append({
                'doobie_type': row.doobie_type,
                'mapping_id': row.mapping_id,
            })

        response.update({
            'status': 'success',
            'doobies': doobies,
        })

        return response

# Below is for the stupid testing
pdb.set_trace()
x = Tags.get_tag('1')