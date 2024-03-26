from SPARQLWrapper import SPARQLWrapper, JSON, POST, BASIC
import logging
import os


class TripleStoreConection:

    def get_count_individuals(self, query):
        try:
            TRIPLESTORE_URL = os.environ['TRIPLESTORE_URL']
            TRIPLESTORE_USERNAME = os.environ['TRIPLESTORE_USERNAME']
            TRIPLESTORE_PASSWORD = os.environ['TRIPLESTORE_PASSWORD']

            ENDPOINT = SPARQLWrapper(TRIPLESTORE_URL)
            ENDPOINT.setHTTPAuth(BASIC)
            ENDPOINT.setCredentials(TRIPLESTORE_USERNAME, TRIPLESTORE_PASSWORD)
            ENDPOINT.setMethod(POST)
            
            ENDPOINT.setQuery(query)
            ENDPOINT.setReturnFormat(JSON)

            result = ENDPOINT.query().convert()
            return result
        except KeyError as ke:
            logging.error("Missing environmental variable:", str(ke))
            raise RuntimeError("Missing environmental variable") from ke
        except Exception as e:
            logging.error("Issue with SPARQL endpoint")
            logging.error(e)
            raise RuntimeError("Issue with SPARQL endpoint") from e