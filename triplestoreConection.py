from SPARQLWrapper import SPARQLWrapper, JSON, POST, BASIC
import logging
import yaml
import os

class TripleStoreConection:

    TRIPLESTORE_URL = os.environ['TRIPLESTORE_URL']
    TRIPLESTORE_USERNAME = os.environ['TRIPLESTORE_USERNAME']
    TRIPLESTORE_PASSWORD = os.environ['TRIPLESTORE_PASSWORD']

    ENDPOINT = SPARQLWrapper(TRIPLESTORE_URL)
    ENDPOINT.setHTTPAuth(BASIC)
    ENDPOINT.setCredentials(TRIPLESTORE_USERNAME, TRIPLESTORE_PASSWORD)
    ENDPOINT.setMethod(POST)

    def get_count(self, query):
        self.ENDPOINT.setQuery(query)
        self.ENDPOINT.setReturnFormat(JSON)
        try:
            result = self.ENDPOINT.query().convert()
        except Exception as e:
            logging.error("Issue with SPARQL endpoint")
            logging.error(e)
            return None
        return result