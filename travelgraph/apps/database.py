import psycopg2 as pgsql
import psycopg2.extras
import pdb

from travelgraph import settings

postgre = pgsql.connect(
            host=settings.pgsql_host,
            user=settings.pgsql_user,
            password=settings.pgsql_password,
            database=settings.pgsql_db,
        )

cursor = postgre.cursor(cursor_factory=psycopg2.extras.DictCursor)
