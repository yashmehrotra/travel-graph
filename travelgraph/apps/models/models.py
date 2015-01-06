import psycopg2 as pgsql
import pdb

from travelgraph import settings

def init_pgsql_db(database=settings.pgsql_db):
    '''
    Initialize a server instance
    '''
    postgre = pgsql.connect(
            host=settings.pgsql_host,
            user=settings.pgsql_user,
            password=settings.pgsql_password,
            database=database,
        )

    return postgre


def create_user(email, password, first_name='John', last_name='Doe', method=None, **kwargs):
    '''
    This function adds user to the database
    '''
    username = first_name + '-' + last_name

    # Add a function which sees how many users of the same name are there
    
    postgre = init_pgsql_db()
    cursor = postgre.cursor()

    #pdb.set_trace()

    query = """INSERT INTO "user" 
        (email, name, password) 
        VALUES ('{0}', '{1}', '{2}')""".format(email, username, password)

    cursor.execute(query)
    postgre.commit()

    return 'Done, also add exception here'
