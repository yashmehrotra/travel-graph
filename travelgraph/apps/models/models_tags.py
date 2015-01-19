import pdb
import json

from travelgraph import settings
from travelgraph.apps.database import postgre, cursor


def get_tag_id(tag):
    
    query = """ SELECT tag_id FROM "tags" 
        WHERE 'tag_value' = '{0}' """.format(
        tag)

    result = cursor.execute(query)


def add_question_to_tag(tag, ques_id):
    
    tag_id = get_tag_id(tag)