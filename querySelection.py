import triplestoreConection
import chevron
from perseo.main import milisec
import sys
from ageCalculation import AgeCalculation

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

            #  SEX FILTER
            if parameter.type == "obo:NCIT_C28421" or parameter.type =="http://purl.obolibrary.org/obo/NCIT_C28421":
                with open('templates/block.mustache', 'r') as f:
                    sexBlock = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'filter':"sex"})
                queryText = queryText + sexBlock

            # DISEASE FILTER
            elif parameter.type == "obo:NCIT_C2991" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C2991":

                if isinstance(parameter.id, list):
                    for param in parameter.id:
                        with open('templates/block.mustache', 'r') as f:
                            stamp = "disease" + milisec()
                            diseaseBlock = chevron.render(f, {'value': param, 'operator': parameter.operator,'filter': stamp})
                        queryText = queryText + diseaseBlock

                else:
                    with open('templates/block.mustache', 'r') as f:
                        stamp = "disease" + milisec()
                        diseaseBlock = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'filter':stamp})
                    queryText = queryText + diseaseBlock

            # PHENOTYPE FILTER
            elif parameter.type == "sio:SIO_010056" or parameter.type == "http://semanticscience.org/resource/SIO_010056":
                if isinstance(parameter.id, list):
                    for param in parameter.id:
                        with open('templates/block.mustache', 'r') as f:
                            stamp = "phenotype" + milisec()
                            phenotypeBlock = chevron.render(f, {'value': param, 'operator': parameter.operator,'filter':stamp})
                        queryText = queryText + phenotypeBlock
                else:
                    with open('templates/block.mustache', 'r') as f:
                        stamp = "phenotype" + milisec()
                        phenotypeBlock = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'filter':stamp})
                    queryText = queryText + phenotypeBlock

            # GENETIC
            elif parameter.type == "edam:data_2295" or parameter.type == "http://edamontology.org/data_2295":
                if isinstance(parameter.id, list):
                    for param in parameter.id:
                        with open('templates/block.mustache', 'r') as f:
                            stamp = "genotype" + milisec()
                            genotypeBlock = chevron.render(f, {'value': param, 'operator': parameter.operator,'filter':stamp})
                        queryText = queryText + genotypeBlock
                else:
                    with open('templates/block.mustache', 'r') as f:
                        stamp = "genotype" + milisec()
                        genotypeBlock = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'filter':stamp})
                    queryText = queryText + genotypeBlock

            # AGE FILTER
            elif parameter.type == "obo:NCIT_C83164" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C83164":
                with open('templates/block_age.mustache', 'r') as f:
                    startdate, enddate = AgeCalculation.calculateBirthdataRange(parameter.id, parameter.operator)
                    ageBlock = chevron.render(f, {'start': startdate, 'end': enddate,'filter':'age'})
                queryText = queryText + ageBlock

            elif parameter.type == "obo:NCIT_C124353" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C124353":
                with open('templates/block_age.mustache', 'r') as f:
                    startdate, enddate = AgeCalculation.calculateBirthdataRange(parameter.id, parameter.operator)
                    startage, endage = AgeCalculation.calculateAgeRange(parameter.id, parameter.operator)
                    symptomBlock = chevron.render(f, {'start': startdate, 'end': enddate,'filter':"date_symptom",'age_start':startage, 'age_end':endage, 'filter_2':'age_symptom' })
                queryText = queryText + symptomBlock



            else:
                sys.exit("Any of the parameters you passed are not corrected, please check you input JSON request body")

        queryText = queryText + "\n" + "}" + "\n"

        # print(queryText)
        result = self.TRIPLE_STORE_CONECTION.get_count(queryText)
        count = result["results"]["bindings"][0]["count"]["value"]
        return count
    


