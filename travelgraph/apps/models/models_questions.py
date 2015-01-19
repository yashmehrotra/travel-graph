import pdb
import json

from travelgraph.apps.database import postgre, cursor
from travelgraph.apps.models import models_tags

def add_question(user_id, api_key,
    question_text, question_desc, question_tags):
    
    response = {}

    # All tags should be low case

    question_tags = question_tags.split(',')
    question_tags = [ str(tag.lower()) for tag in question_tags ]

    question_text = str(question_text)
    question_desc = str(question_desc)
    user_id = str(user_id)

    query = """ INSERT INTO "questions" (question_text, question_desc, question_tags, user_id) 
                 VALUES ('{0}', '{1}', '{2}', '{3}') 
                 RETURNING question_id """.format(
                    question_text, question_desc, json.dumps(question_tags), user_id)

    #pdb.set_trace()
    cursor.execute(query)

    postgre.commit()

    # Take question id and add tags to the main table and connect them

    question_id = cursor.fetchone()[0]

    for tag in question_tags:
        models_tags.add_question_to_tag(tag, question_id)

    response.update({
        'status':'success',
        'message':'question successfully added',
        'question':question_text,
    })

    return response

    