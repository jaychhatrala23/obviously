from elasticsearch_dsl import Q
from .documents import PersonDocument


def elasticsearch_persons(query):
    """
    Perform a fuzzy search for persons based on the full name using Elasticsearch.
    """
    s = PersonDocument.search()
    s = s.query('match', full_name={'query': query, 'fuzziness': 'AUTO'})
    return s.to_queryset()
