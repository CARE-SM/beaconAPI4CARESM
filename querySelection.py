import triplestoreConection
import chevron
from perseo.main import milisec
import sys
import os
# from ageCalculation import AgeCalculation

class QueryBuilder:

    TRIPLE_STORE_CONECTION = triplestoreConection.TripleStoreConection()

    def individuals_query_builder(self, input_data):
        
        FILTER_SEX = str(os.getenv("FILTER_SEX"))
        FILTER_DISEASE = str(os.getenv("FILTER_DISEASE"))
        FILTER_SYMPTOM = str(os.getenv("FILTER_SYMPTOM"))
        FILTER_GENE_VARIANT = str(os.getenv("FILTER_GENE_VARIANT"))
        FILTER_BIRTHYEAR = str(os.getenv("FILTER_BIRTHYEAR"))
        FILTER_AGE_SYMPTOM_ONSET = str(os.getenv("FILTER_AGE_SYMPTOM_ONSET"))
        FILTER_AGE_DIAGNOSIS = str(os.getenv("FILTER_AGE_DIAGNOSIS"))

        with open('templates/block1_SELECT.mustache', 'r') as f:
            queryText = chevron.render(f)

        # Explore all filters that are sent as Request body
        if input_data.query.filters:
            
            list_filters_used = []
            symp_info = {}
            onset_info = {}    
             
            for parameter in input_data.query.filters:
                if parameter.type:
                    list_filters_used += [parameter.type]
            if ("sio:SIO_010056" in list_filters_used or "http://semanticscience.org/resource/SIO_010056" in list_filters_used) and ("obo:NCIT_C124353" in list_filters_used or "http://purl.obolibrary.org/obo/NCIT_C124353" in list_filters_used):
                if (FILTER_SYMPTOM == "True") and (FILTER_AGE_SYMPTOM_ONSET == "True"):
                    for parameter in input_data.query.filters:
                        if parameter.type =="sio:SIO_010056" or parameter.type =="http://semanticscience.org/resource/SIO_010056":
                            symp_info = parameter

                        elif parameter.type == "obo:NCIT_C124353" or parameter.type =="http://purl.obolibrary.org/obo/NCIT_C124353":
                            onset_info = parameter               

                    # Symptom + Symptom Onset FILTER
                    with open('templates/block1b_BIND.mustache', 'r') as f:
                        Block = chevron.render(f, {'value': onset_info.id, 'operator': onset_info.operator ,'cde':"onset", "cde2":"birthdate"})
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
                        Block = chevron.render(f, {'value': "sio:SIO_000614", 'operator': "=" ,'cde':"onset"})
                    queryText = queryText + Block
                    
                    with open('templates/block3c_TARGET.mustache', 'r') as f:
                        Block = chevron.render(f, {'target': symp_info.id, 'operator': symp_info.operator ,'cde':"onset"})
                    queryText = queryText + Block
                
                    with open('templates/block2b_ACTIVITY.mustache', 'r') as f:
                        Block = chevron.render(f, {'activity': "obo:NCIT_C124353",'cde':"onset"})
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
                    sys.exit( "You have used unpermitted filter for this repository, neither SYMPTOM nor AGE OF SYMPTOM ONSET is available")
            for parameter in input_data.query.filters:                
                if parameter.type:
                    # SEX FILTER
                    if parameter.type == "obo:NCIT_C28421" or parameter.type =="http://purl.obolibrary.org/obo/NCIT_C28421":
                        if FILTER_SEX == "True":
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'cde':"sex"})
                            queryText = queryText + Block
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"sex"})
                            queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for SEX is not available")

                    # DISEASE FILTER
                    elif parameter.type == "obo:NCIT_C2991" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C2991":
                        if FILTER_DISEASE == "True":
                            if isinstance(parameter.id, list):
                                for param in parameter.id:
                                    stamp = "disease" + milisec()
                                    with open('templates/block2_GENERAL.mustache', 'r') as f:
                                        Block = chevron.render(f, {'value': param, 'operator': parameter.operator,'cde':stamp})
                                    queryText = queryText + Block
                                    with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                        Block = chevron.render(f, {'cde':stamp})
                                    queryText = queryText + Block
                            else:
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'cde':"disease"})
                                queryText = queryText + Block
                                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':"disease"})
                                queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for DISEASE is not available")


                    # SYMPTOM/PHENOTYPE FILTER
                    elif ("sio:SIO_010056" in list_filters_used or "http://semanticscience.org/resource/SIO_010056" in list_filters_used) and ("obo:NCIT_C124353" not in list_filters_used and "http://purl.obolibrary.org/obo/NCIT_C124353" not in list_filters_used):
                        if FILTER_SYMPTOM == "True":
                            if isinstance(parameter.id, list):
                                for param in parameter.id:
                                    stamp = "phenotype" + milisec()
                                    with open('templates/block2_GENERAL.mustache', 'r') as f:
                                        Block = chevron.render(f, {'value': param, 'operator': parameter.operator,'cde':stamp})
                                    queryText = queryText + Block
                                    with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                        Block = chevron.render(f, {'cde':stamp})
                                    queryText = queryText + Block
                            else:
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator,'cde':"phenotype"})
                                queryText = queryText + Block
                                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':"phenotype"})
                                queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for SYMPTOM/PHENOTYPE is not available")
                        
                    # GENOTYPE FILTER
                    elif parameter.type == "edam:data_2295": 
                        if FILTER_GENE_VARIANT == "True":
                            if isinstance(parameter.id, list):
                                for param in parameter.id:
                                    stamp = "genetic" + milisec()
                                    with open('templates/block2_GENERAL.mustache', 'r') as f:
                                        Block = chevron.render(f, {'value': "sio:SIO_000614", 'operator': '!=' ,'cde':stamp})
                                    queryText = queryText + Block
                                    with open('templates/block3_OUTPUT.mustache', 'r') as f:
                                        Block = chevron.render(f, {'value': param, 'cde':stamp})
                                    queryText = queryText + Block
                                    with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                        Block = chevron.render(f, {'cde':stamp})
                                    queryText = queryText + Block
                            else:
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {'value': "sio:SIO_000614", 'operator': '=' ,'cde':"genetic"})
                                queryText = queryText + Block
                                with open('templates/block3_OUTPUT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'value': parameter.id, 'cde':"genetic"})
                                queryText = queryText + Block
                                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':"genetic"})
                                queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for GENETIC VARIANT is not available")
                        
                        
                    # BIRTHYEAR FILTER:
                    elif parameter.type == "obo:NCIT_C83164" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C83164":
                        if FILTER_BIRTHYEAR == "True":

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
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for BIRTHYEAR is not available")
                        
                    # AGE_OF_SYMPTOM FILTER:
                    elif ("sio:SIO_010056" not in list_filters_used and "http://semanticscience.org/resource/SIO_010056" not in list_filters_used) and ("obo:NCIT_C124353" in list_filters_used or "http://purl.obolibrary.org/obo/NCIT_C124353" in list_filters_used):
                        if FILTER_AGE_SYMPTOM_ONSET == "True":
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
                                Block = chevron.render(f, {'value': "sio:SIO_000614", 'operator': "=" ,'cde':"onset"})
                            queryText = queryText + Block
                            with open('templates/block2b_ACTIVITY.mustache', 'r') as f:
                                Block = chevron.render(f, {'activity': "obo:NCIT_C124353",'cde':"onset"})
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
                            sys.exit( "You have used unpermitted filter for this repository, filter for AGE OF SYMPTOM ONSET is not available")

                    # AGE_AT_DIAGNOSIS:
                    elif parameter.type == "obo:NCIT_C156420" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C156420":
                        if FILTER_AGE_DIAGNOSIS == "True":

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
                            sys.exit("You have used unpermitted filter for this repository, filter for AGE OF DIAGNOSIS is not available")                            
                            
                else:
                    if FILTER_DISEASE == "True":
                        if isinstance(parameter.id, list):
                            for param in parameter.id:
                                stamp = "disease" + milisec()
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {'value': param, 'operator': '=','cde':stamp})
                                queryText = queryText + Block
                                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':stamp})
                                queryText = queryText + Block
                        else:
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {'value': parameter.id, 'operator': '=','cde':"disease"})
                            queryText = queryText + Block
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"disease"})
                            queryText = queryText + Block
                    else:
                        sys.exit( "You have used unpermitted filter for this repository, filter for DISEASE is not available")   

            with open('templates/block6_CLOSE.mustache', 'r') as f:
                Block = chevron.render(f, {})
            queryText = queryText + Block
        else:
            sys.exit("Any of the parameters you passed is not corrected, please check you input JSON request body")
            
        # stamp_file = "file" + milisec() + ".ttl"
        # f = open(stamp_file, "a")
        # f.write(queryText)
        # f.close()
        
        # print(queryText)
        
        result = self.TRIPLE_STORE_CONECTION.get_count_individuals(queryText)
        count = result["results"]["bindings"][0]["count"]["value"]
        return count
    
    # def catalog_query_builder(self,input_data):

    #     endpoint = ""
    #     with open('templates/catalog1_SELECT.mustache', 'r') as f:
    #         queryText = chevron.render(f)


    #     if input_data.query.filters:
    #     # Explore all filters that are sent as Request body
    #         for parameter in input_data.query.filters:
    #             if parameter.type:
    #                 # RESOURCE_TYPE FILTER
    #                 if parameter.type == "rdf:type":
    #                     # stamp = "theme" + milisec()
    #                     with open('templates/catalog2a_RESOURCE_TYPE.mustache', 'r') as f:
    #                         Block = chevron.render(f, {'resource_type': parameter.id})
    #                     queryText = queryText + Block

    #                 # THEME FILTER
    #                 elif parameter.type == "dcat:theme" or parameter.type =="http://www.w3.org/ns/dcat#theme":
    #                     stamp = "theme" + milisec()
    #                     with open('templates/catalog2b_THEME.mustache', 'r') as f:
    #                         Block = chevron.render(f, {'theme': parameter.id,'stamp':stamp})
    #                     queryText = queryText + Block
    #             else:
    #                 # THEME FILTER
    #                 stamp = "theme" + milisec()
    #                 with open('templates/catalog2b_THEME.mustache', 'r') as f:
    #                     Block = chevron.render(f, {'theme': parameter.id,'stamp':stamp})
    #                 queryText = queryText + Block

    #                 # # ID for endpoint
    #                 # elif parameter.type == "dct:identifier" or parameter.type =="http://purl.org/dc/terms/identifier":
    #                 #     endpoint = parameter.id
            
    #         with open('templates/catalog3_CLOSE.mustache', 'r') as f:
    #             Block = chevron.render(f, {})
    #         queryText = queryText + Block
    #     else:
    #         sys.exit("Any of the parameters you passed are not corrected, please check you input JSON request body")

    #     # if endpoint == "":
    #     #     sys.exit("No ID was defined at filters, so no endpoint is associated to this call")
        
    #     print(queryText)
    #     result = self.TRIPLE_STORE_CONECTION.get_count_catalogs(queryText, endpoint=endpoint)

    #     count = len(result["results"]["bindings"])

    #     does_data_exist = False
    #     if count is not 0:
    #         does_data_exist = True

    #     resulting_dict = {"resultSets":[]}

    #     for row in result["results"]["bindings"]:
    #         data_per_row = {
    #             'id': "undefined resultset ID",
    #             'setType': "undefined set type",
    #             'exists': does_data_exist,
    #             "resultsCount": 1,
    #             "results": []
    #         }

    #         data_per_result = {
    #             "title" : row["name"]["value"],
    #             "description": row["description"]["value"],
    #             "resourceTypes": row["resource_type"]["value"],
    #             "version": row["version"]["value"]
    #         }

    #         data_per_row["results"].append(data_per_result)
    #         resulting_dict["resultSets"].append(data_per_row)
            

    #     return [count, resulting_dict]




