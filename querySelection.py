import triplestoreConection
import chevron
from perseo.main import milisec
import sys
# from ageCalculation import AgeCalculation

class QuerySelection:

    TRIPLE_STORE_CONECTION = triplestoreConection.TripleStoreConection()

    def individualsCountingQuery(self, input_data):
        """
        Counting for individuals, creates modular SPARQL queries based on EJP CDE semantic models. Parameters are passed as request body where you define what data elements are you searching for. \n
        Specifications can be found here: https://github.com/ejp-rd-vp/vp-api-specs \n
        """



        with open('templates/block1_SELECT.mustache', 'r') as f:
            queryText = chevron.render(f)

        # Explore all filters that are sent as Request body
        for parameter in input_data.properties.query.filters:

            # SEX FILTER
            if parameter.type == "obo:NCIT_C28421" or parameter.type =="http://purl.obolibrary.org/obo/NCIT_C28421":
                with open('templates/block2_GENERAL.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'cde':"sex"})
                queryText = queryText + Block
                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"sex"})
                queryText = queryText + Block


            # DISEASE FILTER
            elif parameter.type == "obo:NCIT_C2991" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C2991":

                if isinstance(parameter.id, list):
                    for param in parameter.id:
                        stamp = "disease" + milisec()
                        with open('templates/block2_GENERAL.mustache', 'r') as f:
                            Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'cde':stamp})
                        queryText = queryText + Block
                        with open('templates/block5_CONTEXT.mustache', 'r') as f:
                            Block = chevron.render(f, {'value': parameter.id, 'cde':stamp})
                        queryText = queryText + Block
                else:
                    with open('templates/block2_GENERAL.mustache', 'r') as f:
                        Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'cde':"disease"})
                    queryText = queryText + Block
                    with open('templates/block5_CONTEXT.mustache', 'r') as f:
                        Block = chevron.render(f, {'cde':"disease"})
                    queryText = queryText + Block


            # PHENOTYPE FILTER
            elif parameter.type == "sio:SIO_010056" or parameter.type == "http://semanticscience.org/resource/SIO_010056":

                if isinstance(parameter.id, list):
                    for param in parameter.id:
                        stamp = "phenotype" + milisec()
                        with open('templates/block2_GENERAL.mustache', 'r') as f:
                            Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'cde':stamp})
                        queryText = queryText + Block
                        with open('templates/block5_CONTEXT.mustache', 'r') as f:
                            Block = chevron.render(f, {'value': parameter.id, 'cde':stamp})
                        queryText = queryText + Block
                else:
                    with open('templates/block2_GENERAL.mustache', 'r') as f:
                        Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'cde':"phenotype"})
                    queryText = queryText + Block
                    with open('templates/block5_CONTEXT.mustache', 'r') as f:
                        Block = chevron.render(f, {'cde':"phenotype"})
                    queryText = queryText + Block

            # GENOTYPE FILTER
            elif parameter.type == "edam:data_2295": 

                if isinstance(parameter.id, list):
                    for param in parameter.id:
                        stamp = "genetic" + milisec()
                        with open('templates/block2_GENERAL.mustache', 'r') as f:
                            Block = chevron.render(f, {'value': "sio:SIO_000614", 'operator': '!=' ,'cde':stamp})
                        queryText = queryText + Block
                        with open('templates/block3_OUTPUT.mustache', 'r') as f:
                            Block = chevron.render(f, {'value': parameter.id, 'cde':stamp})
                        queryText = queryText + Block
                        with open('templates/block5_CONTEXT.mustache', 'r') as f:
                            Block = chevron.render(f, {'cde':stamp})
                        queryText = queryText + Block
                else:
                    with open('templates/block2_GENERAL.mustache', 'r') as f:
                        Block = chevron.render(f, {'value': "sio:SIO_000614", 'operator': '!=' ,'cde':"genetic"})
                    queryText = queryText + Block
                    with open('templates/block3_OUTPUT.mustache', 'r') as f:
                        Block = chevron.render(f, {'value': parameter.id, 'cde':"genetic"})
                    queryText = queryText + Block
                    with open('templates/block5_CONTEXT.mustache', 'r') as f:
                        Block = chevron.render(f, {'cde':"genetic"})
                    queryText = queryText + Block

            # BIRTHYEAR FILTER:
            elif parameter.type == "obo:NCIT_C83164" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C83164":

                with open('templates/block2_GENERAL.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': parameter.type, 'operator': '=' ,'cde':"age"})
                queryText = queryText + Block
                with open('templates/block3b_OUTPUT_VALUE.mustache', 'r') as f:
                    # startage, endage = AgeCalculation.calculateAgeRange(parameter.id, parameter.operator)
                    Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator, 'cde':"age"})
                queryText = queryText + Block
                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"age"})
                queryText = queryText + Block

            # AGE_OF_SYMPTOM FILTER:
            elif parameter.type == "obo:NCIT_C124353" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C124353":

                with open('templates/block1b_BIND.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator ,'cde':"onset", "cde2":"birthdate"})
                queryText = queryText + Block
                with open('templates/block2_GENERAL.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': "obo:NCIT_C68615", 'operator': "=" ,'cde':"birthdate"})
                queryText = queryText + Block
                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"birthdate"})
                queryText = queryText + Block
                with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"birthdate"})
                queryText = queryText + Block
                with open('templates/block2_GENERAL.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': "obo:NCIT_C124353", 'operator': "=" ,'cde':"onset"})
                queryText = queryText + Block
                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"onset"})
                queryText = queryText + Block
                with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"onset"})
                queryText = queryText + Block
                with open('templates/block6_CLOSE.mustache', 'r') as f:
                    Block = chevron.render(f, {})
                queryText = queryText + Block
                with open('templates/block6_CLOSE.mustache', 'r') as f:
                    Block = chevron.render(f, {})
                queryText = queryText + Block

            # AGE_AT_DIAGNOSIS:
            elif parameter.type == "obo:NCIT_C156420" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C156420":

                with open('templates/block1b_BIND.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator ,'cde':"onset", "cde2":"birthdate"})
                queryText = queryText + Block
                with open('templates/block2_GENERAL.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': "obo:NCIT_C68615", 'operator': "=" ,'cde':"birthdate"})
                queryText = queryText + Block
                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"birthdate"})
                queryText = queryText + Block
                with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"birthdate"})
                queryText = queryText + Block
                with open('templates/block2_GENERAL.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': "sio:SIO_000614", 'operator': "!=" ,'cde':"onset"})
                queryText = queryText + Block
                with open('templates/block4_ATTRIBUTE2.mustache', 'r') as f:
                    Block = chevron.render(f, {'value': "obo:NCIT_C2991 ",'cde':"onset"})
                queryText = queryText + Block
                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"onset"})
                queryText = queryText + Block
                with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                    Block = chevron.render(f, {'cde':"onset"})
                queryText = queryText + Block
                with open('templates/block6_CLOSE.mustache', 'r') as f:
                    Block = chevron.render(f, {})
                queryText = queryText + Block
                with open('templates/block6_CLOSE.mustache', 'r') as f:
                    Block = chevron.render(f, {})
                queryText = queryText + Block

            else:
                sys.exit("Any of the parameters you passed are not corrected, please check you input JSON request body")

        with open('templates/block6_CLOSE.mustache', 'r') as f:
            Block = chevron.render(f, {})
        queryText = queryText + Block

        print(queryText)
        result = self.TRIPLE_STORE_CONECTION.get_count_individuals(queryText)
        count = result["results"]["bindings"][0]["count"]["value"]
        return count
    
    def catalogCountingQuery(self,input_data):

        endpoint = ""
        with open('templates/catalog1_SELECT.mustache', 'r') as f:
            queryText = chevron.render(f)

        # Explore all filters that are sent as Request body
        for parameter in input_data.properties.query.filters:

            # RESOURCE_TYPE FILTER
            if parameter.type == "rdf:type":
                # stamp = "theme" + milisec()
                with open('templates/catalog2a_RESOURCE_TYPE.mustache', 'r') as f:
                    Block = chevron.render(f, {'resource_type': parameter.id})
                queryText = queryText + Block

            # THEME FILTER
            elif parameter.type == "dcat:theme" or parameter.type =="http://www.w3.org/ns/dcat#theme":
                stamp = "theme" + milisec()
                with open('templates/catalog2b_THEME.mustache', 'r') as f:
                    Block = chevron.render(f, {'theme': parameter.id,'stamp':stamp})
                queryText = queryText + Block

            # ID for endpoint
            elif parameter.type == "dct:identifier" or parameter.type =="http://purl.org/dc/terms/identifier":
                endpoint = parameter.id
        
        with open('templates/catalog3_CLOSE.mustache', 'r') as f:
            Block = chevron.render(f, {})
        queryText = queryText + Block


        if endpoint == "":
            sys.exit("No ID was defined at filters, so no endpoint is associated to this call")
        

        result = self.TRIPLE_STORE_CONECTION.get_count_catalogs(queryText, endpoint=endpoint)
        return result




