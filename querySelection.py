import triplestoreConection
import chevron

class QuerySelection:

    TRIPLE_STORE_CONECTION = triplestoreConection.TripleStoreConection()

    def individualsCountingQuery(self, input_data):
        """
        Counting for individuals, creates modular SPARQL queries based on EJP CDE semantic models. Parameters are passed as request body where you define what data elements are you searching for. \n
        Specifications can be found here: https://github.com/ejp-rd-vp/vp-api-specs \n
        It retrieves JSON object that defines counted individuals as {"count" : nº of individuals} \n
        """

        with open('templates/basicTemplate.mustache', 'r') as f:
            queryText = chevron.render(f)

        # Explore all filters that are sent as Request body
        for parameter in input_data.properties.query.filters:

            # In case of Sex filter is called:
            if parameter.types == "obo:NCIT_C28421":
                with open('templates/sexTemplate.mustache', 'r') as f:
                    sexBlock = chevron.render(f, {'sexReference': parameter.ids})

                queryText = queryText + sexBlock

            # In case of Disease filter is called:
            elif parameter.types == "sio:SIO_001003":
                with open('templates/diseaseTemplate.mustache', 'r') as f:
                    diseaseBlock = chevron.render(f, {'diseaseReference': parameter.ids})

                queryText = queryText + diseaseBlock
        queryText = queryText + "\n" + "}" + "\n"


        result = self.TRIPLE_STORE_CONECTION.get_count(queryText)
        count = result["results"]["bindings"][0]["count"]["value"]
        return count

