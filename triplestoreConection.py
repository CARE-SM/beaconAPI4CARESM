from SPARQLWrapper import SPARQLWrapper, JSON, POST, BASIC
import logging
import yaml

class TripleStoreConection:

    yaml_config = open("config.yaml")
    configuration = yaml.load(yaml_config, Loader=yaml.FullLoader)

    ENDPOINT = SPARQLWrapper(configuration["TRIPLESTORE_URL"])
    ENDPOINT.setHTTPAuth(BASIC)
    ENDPOINT.setCredentials(configuration["TRIPLESTORE_USERNAME"], configuration["TRIPLESTORE_PASSWORD"])
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