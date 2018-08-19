import logging
from common.util.sql_util import enrich_sql
from engine.generator.generator import Generator
from common.util.common_util import extract_query_and_predicate_from

LOGGER = logging.getLogger(__name__)

class QueryGenerator(Generator):

    def __init__(self):
        pass

    def generate(self,data):
        predicate,query = extract_query_and_predicate_from(data)

        if predicate in ('list','value'):
            return query
        else:
            return enrich_sql(query)


