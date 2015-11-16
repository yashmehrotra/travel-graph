# Global Website Settings
WEBSITE_NAME = 'Ghoom'
WEBSITE_URL = 'http://www.ghoom.co'

# Authentication Settings
AUTH_KEY_NAMESPACE = 'db_auth_key'
ACCESS_TOKEN_NAMESPACE = 'db_access_token'

# Redis Settings
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_AUTH_KEY_DB = 0
REDIS_ACCESS_TOKEN_DB = 0

# PostgreSQL Settings
PGSQL_USER = 'test_user_1'
PGSQL_PASSWORD = 'test'
PGSQL_HOST = 'localhost'
PGSQL_PORT = 5432
PGSQL_DATABASE = 'db_test_1'

SQLALCHEMY_ENGINE = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(PGSQL_USER,
                                                              PGSQL_PASSWORD,
                                                              PGSQL_HOST,
                                                              PGSQL_PORT,
                                                              PGSQL_DATABASE)

# Mandrill Email Client Settings
MANDRILL_API_KEY = 'Dp007bLY1BZ6UnR7W4uIhA'

# Facebook Authentication
FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'

# Gearman Settings
GEARMAN_SWITCH = True
GEARMAN_HOST = ''
GEARMAN_PORT = 4730

# Elasticsearch settings
ES_HOST = 'localhost'
ES_PORT = 9200
