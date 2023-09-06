from SPARQLWrapper import SPARQLWrapper, JSON, POST, BASIC
import logging
import yaml
import os

class TripleStoreConection:

    def get_count_individuals(self, query):

        TRIPLESTORE_URL = "https://graphdb.ejprd.semlab-leiden.nl/repositories/unifiedCDE_model"
        TRIPLESTORE_USERNAME = "pabloa"
        TRIPLESTORE_PASSWORD = "ejprdejprd"

        ENDPOINT = SPARQLWrapper(TRIPLESTORE_URL)
        ENDPOINT.setHTTPAuth(BASIC)
        ENDPOINT.setCredentials(TRIPLESTORE_USERNAME, TRIPLESTORE_PASSWORD)
        ENDPOINT.setMethod(POST)


        ENDPOINT.setQuery(query)
        ENDPOINT.setReturnFormat(JSON)

        try:
            result = ENDPOINT.query().convert()
        except Exception as e:
            logging.error("Issue with SPARQL endpoint")
            logging.error(e)
            return None
        print(result)
        return result
    

    def get_count_catalogs(self, query, endpoint):


        ENDPOINT = SPARQLWrapper(endpoint)
        ENDPOINT.setHTTPAuth(BASIC)
        # ENDPOINT.setCredentials(TRIPLESTORE_USERNAME, TRIPLESTORE_PASSWORD)
        ENDPOINT.setMethod(POST)


        ENDPOINT.setQuery(query)
        ENDPOINT.setReturnFormat(JSON)

        # try:
        #     result = ENDPOINT.query().convert()
        # except Exception as e:
        #     logging.error("Issue with SPARQL endpoint")
        #     logging.error(e)
        #     return None
        # print(result)
        return ENDPOINT
    