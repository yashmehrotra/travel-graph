from elasticsearch import Elasticsearch

from verak.settings import (
    ES_ADDRESS,
    ES_INDEX,
    ES_DOC_TYPE_DOOBIE
)


def index_es(doobie):
    """
    Indexes the given serialized doobie to elasticsearch
    """

    es = Elasticsearch(ES_ADDRESS)
    try:
        index_response = es.index(index=ES_INDEX,
                                  doc_type=ES_DOC_TYPE_DOOBIE,
                                  id=doobie.doobie_id,
                                  body=doobie.serialize)

        print 'Indexed {0}:{1}'.format(doobie.serialize['type'],
                                       doobie.serialize['id'])
    except Exception as e:
        print 'problem with indexing - ' + e
