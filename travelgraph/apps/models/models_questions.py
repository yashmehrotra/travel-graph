from travelgraph.apps.database import postgre, cursor
from travelgraph.apps.models import models_tags

def add_question(user_id, user_key,
    question_text, question_desc, question_tags):
    
    response = {}

    # All tags should be low case
    question_tags = [ tag.lower() for tag in question_tags ]

    query = """INSERT INTO "table"
                (question_text, question_desc, question_tags, user_id)
                VALUES ('{0}', '{1}', '{2}', '{3}')""".format(
                    question_text, question_desc, question_tags, user_id)

    cursor.execute(query)

    cursor.commit()

    # Take question id and add tags to the main table and connect them

    question_id = cursor.lastrowid

    for tag in question_tags:
        models_tags.add_question_to_tag(tag, question_id)

    