import triplestoreConection
import chevron

class QuerySelection:

    TRIPLE_STORE_CONECTION = triplestoreConection.TripleStoreConection()

    def individualsCountingQuery(self, input_data):
        """
        Counting for individuals, creates modular SPARQL queries based on EJP CDE semantic models. Parameters are passed as request body where you define what data elements are you searching for. \n
        Specifications can be found here: https://github.com/ejp-rd-vp/vp-api-specs \n
        """

        with open('templates/basic.mustache', 'r') as f:
            queryText = chevron.render(f)

        # Explore all filters that are sent as Request body
        for parameter in input_data.properties.query.filters:

            # In case of Sex filter is called:
            if parameter.type == "obo:NCIT_C28421":# "http://purl.obolibrary.org/obo/NCIT_C28421"
                with open('templates/block.mustache', 'r') as f:
                    sexBlock = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'filter':"sex"})
                queryText = queryText + sexBlock

            # In case of Disease filter is called:
            elif parameter.type == "obo:NCIT_C2991": # "http://purl.obolibrary.org/obo/NCIT_C2991"
                with open('templates/block.mustache', 'r') as f:
                    diseaseBlock = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'filter':"disease"})
                queryText = queryText + diseaseBlock

            # In case of Phenotype filter is called:
            elif parameter.type == "sio:SIO_010056": # "https://sio.semanticscience.org/resource/SIO_010056"
                with open('templates/block.mustache', 'r') as f:
                    phenotypeBlock = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'filter':"phenotype"})
                queryText = queryText + phenotypeBlock
        queryText = queryText + "\n" + "}" + "\n"
        
        # TODO Add filters for Birth year/Age of diagnosis/Symptom/ Gene Ids
        print(queryText)
        result = self.TRIPLE_STORE_CONECTION.get_count(queryText)
        count = result["results"]["bindings"][0]["count"]["value"]
        return count