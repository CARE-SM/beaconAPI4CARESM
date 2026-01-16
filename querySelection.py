import triplestoreConection
import chevron
import sys
import os

class QueryBuilder:
    
    TRIPLE_STORE_CONECTION = triplestoreConection.TripleStoreConnection(
        # endpoint_url="https://graphdb.ejprd.semlab-leiden.nl/repositories/unifiedCDE_model",
        # username="",
        # password="",
    )

    FILTER_SEX = os.getenv("FILTER_SEX","True")
    FILTER_DISEASE = os.getenv("FILTER_DISEASE","True")
    FILTER_SYMPTOM = os.getenv("FILTER_SYMPTOM","True")
    FILTER_GENE_VARIANT = os.getenv("FILTER_GENE_VARIANT","True")
    FILTER_BIRTHYEAR = os.getenv("FILTER_BIRTHYEAR","True")
    FILTER_AGE_SYMPTOM_ONSET = os.getenv("FILTER_AGE_SYMPTOM_ONSET","True")
    FILTER_AGE_DIAGNOSIS = os.getenv("FILTER_AGE_DIAGNOSIS","True")
    
    def filtering_CURIE(self):
        permitted_terms = []
        curie_formats = []
        
        obo_curie_format={
            "id": "ncit",
            "name": "NCIT",
            "url": "http://purl.obolibrary.org/obo/ncit.owl",
            "version": "2023-101-19",
            "namespacePrefix": "obo",
            "iriPrefix": "http://purl.obolibrary.org/obo/"
        }
        curie_formats.append(obo_curie_format)   
        
        if self.FILTER_SEX == "True":
            sex_resource={
                "id": "ncit:C28421",
                "label": "Sex",
                "type": "ontology",
                "scopes": [
                "individuals"
                ]
            }
            permitted_terms.append(sex_resource)    
            
        if self.FILTER_DISEASE == "True":
            disease_resource={
                "id": "ncit:C2991",
                "label": "Disease or Disorder",
                "type": "ontology",
                "scopes": [
                "individuals"
                ]
            }  
            permitted_terms.append(disease_resource)   
            
            ordo_curie={
                "id": "ordo",
                "name": "Orphanet Ontology",
                "url": "https://www.orphadata.com/data/ontologies/ordo/last_version/ORDO_en_4.4.owl",
                "version": "4.4",
                "namespacePrefix": "ordo",
                "iriPrefix": "http://www.orpha.net/ORDO/"
            }
            curie_formats.append(ordo_curie)   

        if self.FILTER_SYMPTOM == "True":
            phenotype_resource={
                "id": "sio:SIO_010056",
                "label": "Phenotype",
                "type": "ontology",
                "scopes": [
                "individuals"
                ]
            }  
            permitted_terms.append(phenotype_resource)    
            
            hpo_curie={
                "id": "hp",
                "name": "Human Phenotype Ontology",
                "url": "http://purl.obolibrary.org/obo/hp.owl",
                "version": "2024-07-01",
                "namespacePrefix": "hp",
                "iriPrefix": "http://purl.obolibrary.org/obo/HP_"
            }
            curie_formats.append(hpo_curie) 
            
            sio_curie={
                "id": "sio",
                "name": "Semanticscience Integrated Ontology",
                "url": "http://semanticscience.org/ontology/sio/v1.59/sio-release.owl",
                "version": "1.59",
                "namespacePrefix": "sio",
                "iriPrefix": "http://semanticscience.org/resource/"
            }
            curie_formats.append(sio_curie)   

        if self.FILTER_GENE_VARIANT == "True":
            genotype_resource={
                "id": "edam:data_2295",
                "label": "Causative Genes",
                "type": "alphanumerical",
                "scopes": [
                "individuals"
                ]
            }
            permitted_terms.append(genotype_resource) 
            
            edam_curie={
                "id": "edam",
                "name": "EDAM",
                "url": "https://edamontology.org/EDAM_1.25.owl",
                "version": "1.21",
                "namespacePrefix": "edam",
                "iriPrefix": "http://edamontology.org/"
            }
            curie_formats.append(edam_curie)   
            
        if self.FILTER_BIRTHYEAR == "True":
            birthyear_resource={
                "id": "ncit:C83164",
                "label": "Age this year",
                "type": "numeric",
                "scopes": [
                "individuals"
                ]
            }
            permitted_terms.append(birthyear_resource) 

        if self.FILTER_AGE_SYMPTOM_ONSET == "True":
            symptom_onset_resource={
                "id": "ncit:C124353",
                "label": "Age at symptom onset",
                "type": "numeric",
                "scopes": [
                "individuals"
                ]
            }           
            permitted_terms.append(symptom_onset_resource) 
            
        if self.FILTER_AGE_DIAGNOSIS == "True":
            age_diagnosis_onset_resource={
                "id": "ncit:C156420",
                "label": "Age at diagnosis",
                "type": "numeric",
                "scopes": [
                    "individuals"
                ]
            }
            permitted_terms.append(age_diagnosis_onset_resource)
            
        return permitted_terms, curie_formats
    
    def detect_number_type(self, string):
        try:
            # Try converting to integer
            int_value = int(string)
            return int_value
        except ValueError():
            sys.exit("Fractional numbers are not allowed")
    
    def curate_values(self, values, tag):
        
        if tag == "ont":            
            if isinstance(values, str):
                curated_values = values
                
            elif isinstance(values, list):
                curated_values = [f"{value} " for value in values]
            
        elif tag == "lit":
            if isinstance(values, str):
                curated_values = [f"'{values}'"]
                
            elif isinstance(values, list):
                curated_values = [f"'{value}'" for value in values]
        else:
            sys.exit("No tag assigned.")
        return " ".join(curated_values)
    
    def individuals_query_builder(self, input_data):

        with open('templates/block1_SELECT.mustache', 'r') as f:
            queryText = chevron.render(f)

        if input_data.query.filters:
            
            list_filters_used = []
            # symp_info = {}
            # onset_info = {}
            
            # Store parameter.types to for later validation
            for parameter in input_data.query.filters:
                if parameter.type:
                    list_filters_used += [parameter.type]
                                        
            for i, parameter in enumerate(input_data.query.filters):

                if parameter.type:
                    
                    # SEX FILTER
                    if parameter.type == "obo:NCIT_C28421" or parameter.type =="http://purl.obolibrary.org/obo/NCIT_C28421":
                        if self.FILTER_SEX == "True":
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                    'process': "sio:SIO_000006",
                                    'operator_attribute': parameter.operator,
                                    'attribute':parameter.id,
                                    'instance': "output_type",
                                    'operator_output': "=",
                                    'output': "obo:NCIT_C160908",
                                    'cde':"sex"})
                            queryText = queryText + Block
                            queryText = queryText + "}"
                        else:
                            sys.exit( "SEX ({parameter.type}) filter not permitted.")

                    # DISEASE FILTER
                    elif parameter.type == "obo:NCIT_C2991" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C2991":
                        if self.FILTER_DISEASE == "True":                            
                            stamp = f"f_disease_{i}"

                            if isinstance(parameter.id, str):
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "obo:NCIT_C18020",
                                        'operator_attribute': "=",
                                        'attribute': "obo:NCIT_C7057",
                                        'instance': "output_identifier",
                                        'operator_output': parameter.operator,
                                        'output': parameter.id,
                                        'cde':stamp})  
                                queryText = queryText + Block                          
                                queryText = queryText + "}"

                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id, tag="ont")

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "obo:NCIT_C18020",
                                        'operator_attribute': "=",
                                        'attribute': "obo:NCIT_C7057",
                                        'instance': "output_type",
                                        'operator_output': "=",
                                        'output': "obo:OGMS_0000073",
                                        'cde': stamp})                                      
                                queryText = queryText + Block
                                                                
                                with open('templates/block3c_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "output_identifier",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block
                                queryText = queryText + "}"
                                
                        else:
                            sys.exit( "DISEASE ({parameter.type}) filter not permitted.")

                    # PHENOTYPE FILTER
                    elif parameter.type == "sio:SIO_010056" or parameter.type == "http://semanticscience.org/resource/SIO_010056":
                        if self.FILTER_SYMPTOM == "True":
                            stamp = f"f_phenotype_{i}"

                            if isinstance(parameter.id, str):
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "obo:NCIT_C18020",
                                        'operator_attribute': "=",
                                        'attribute': "sio:SIO_000614",
                                        'instance': "output_identifier",
                                        'operator_output': parameter.operator,
                                        'output': parameter.id,
                                        'cde':stamp}) 
                                queryText = queryText + Block
                                queryText = queryText + "}"
                                                                       
                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id, tag="ont")

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "obo:NCIT_C18020",
                                        'operator_attribute': "=",
                                        'attribute': "sio:SIO_000614",
                                        'instance': "output_type",
                                        'operator_output': "=",
                                        'output': "obo:NCIT_C16977",
                                        'cde':stamp})     
                                queryText = queryText + Block
                                    
                                with open('templates/block3c_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "output_identifier",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block  
                                queryText = queryText + "}"

                        else:
                            sys.exit( "PHENOTYPE ({parameter.type}) filter not permitted.")
                        
                    # GENOTYPE FILTER
                    elif parameter.type == "edam:data_2295": 
                        if self.FILTER_GENE_VARIANT == "True":
                            stamp = f"f_genetic_{i}"

                            if isinstance(parameter.id, str) or isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id, tag="lit")

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "obo:NCIT_C15709",
                                        'operator_attribute': "=",
                                        'attribute': "sio:SIO_000614",
                                        'instance': "output_type",
                                        'operator_output': "=",
                                        'output': "obo:NCIT_C171178",
                                        'cde':stamp})
                                queryText = queryText + Block
                                
                                with open('templates/block3a_HASVALUE.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':stamp, 'instance':"output_identifier"})
                                queryText = queryText + Block
                                
                                with open('templates/block3c_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "value",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block 
                                queryText = queryText + "}"
                            
                        else:
                            sys.exit( "GENETIC VARIANT ({parameter.type}) filter not permitted.")

                    # BIRTHYEAR FILTER
                    elif parameter.type == "obo:NCIT_C83164" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C83164":
                        if self.FILTER_BIRTHYEAR == "True":
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "sio:SIO_000006",
                                            'operator_attribute': "=",
                                            'attribute': parameter.type,
                                            'instance': "output_type",
                                            'operator_output': "=",
                                            'output': "sio:SIO_000015",
                                            'cde':"birthyear"})                                                                        
                            queryText = queryText + Block
                            
                            with open('templates/block3a_HASVALUE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"birthyear", 'instance':"output"})
                            queryText = queryText + Block                         
                            
                            with open('templates/block3b_DATATYPE.mustache', 'r') as f:
                                Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator, 'datatype':"xsd:integer", 'cde':"birthyear"})
                            queryText = queryText + Block
                            queryText = queryText + "}"
                        else:
                            sys.exit( "YBIRTHYEAR ({parameter.type}) filter not permitted.")
                        
                    # AGE_OF_SYMPTOM FILTER
                    elif parameter.type == "sio:SIO_010056" or parameter.type == "http://semanticscience.org/resource/SIO_010056":
                        if self.FILTER_AGE_SYMPTOM_ONSET == "True":
                            
                            parameter_checked = self.detect_number_type(parameter.id)
                            
                            with open('templates/block1b_BIND.mustache', 'r') as f:
                                Block = chevron.render(f, {'value': parameter_checked, 'operator': parameter.operator ,'st':"s_",'cde':"s_onset", "cde2":"s_birthdate"})
                            queryText = queryText + Block
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "sio:SIO_000006",
                                            'operator_attribute': "=",
                                            'attribute': "obo:NCIT_C68615",
                                            'instance': "output_type",
                                            'operator_output': "=",
                                            'output': "sio:SIO_000015",
                                            'cde':"s_birthdate"})   
                            queryText = queryText + Block
                            with open('templates/block4_STARTDATE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"s_birthdate"})
                            queryText = queryText + Block
                            
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "sio:SIO_000006",
                                            'operator_attribute': "=",
                                            'attribute': "obo:NCIT_C124353",
                                            'instance': "output_type",
                                            'operator_output': "=",
                                            'output': "sio:SIO_000015",
                                            'cde':"s_onset"})  
                            queryText = queryText + Block           
                            with open('templates/block4_STARTDATE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"s_onset"})
                            queryText = queryText + Block
                            queryText = queryText + "}"
                            queryText = queryText + "}"
                        else:
                            sys.exit( "AGE OF SYMPTOM ONSET ({parameter.type}) filter not permitted.")

                    # AGE_AT_DIAGNOSIS FILTER
                    elif parameter.type == "obo:NCIT_C156420" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C156420":
                        if self.FILTER_AGE_DIAGNOSIS == "True":
                            
                            parameter_checked = self.detect_number_type(parameter.id)

                            with open('templates/block1b_BIND.mustache', 'r') as f:
                                Block = chevron.render(f, {'value': parameter_checked, 'operator': parameter.operator ,'st':"d_",'cde':"d_onset", "cde2":"d_birthdate"})
                            queryText = queryText + Block
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "sio:SIO_000006",
                                            'operator_attribute': "=",
                                            'attribute': "obo:NCIT_C68615",
                                            'operator_output': "=",
                                            'instance': "output_type",
                                            'output': "sio:SIO_000015",
                                            'cde':"d_birthdate"})                                                                         
                            queryText = queryText + Block
                            with open('templates/block4_STARTDATE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"d_birthdate"})
                            queryText = queryText + Block
                                                        
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "obo:NCIT_C18020",
                                            'operator_attribute': "=",
                                            'attribute': "obo:NCIT_C7057",
                                            'instance': "output_type",
                                            'operator_output': "=",
                                            'output': "obo:OGMS_0000073",
                                            'cde':"d_onset"})  
                            queryText = queryText + Block
                            with open('templates/block4_STARTDATE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"d_onset"})
                            queryText = queryText + Block
                            queryText = queryText + "}"
                            queryText = queryText + "}" 
                            
                        else:
                            sys.exit("AGE OF DIAGNOSIS ({parameter.type}) filter not permitted.")                            
                            
                else:
                    # DISEASE FILTER
                    # Disease is the default filter, even if parameter.type is defined or not.
                    if self.FILTER_DISEASE == "True":
                        stamp = f"f_disease_{i}"

                        if isinstance(parameter.id, str):
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                    'process': "obo:NCIT_C18020",
                                    'operator_attribute': "=",
                                    'attribute': "obo:NCIT_C7057",
                                    'instance': "output_identifier",
                                    'operator_output': "=",
                                    'output': parameter.id,
                                    'cde':stamp})  
                            queryText = queryText + Block                          
                            queryText = queryText + "}"

                        elif isinstance(parameter.id, list):
                            curated_values = self.curate_values(parameter.id, tag="ont")

                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                    'process': "obo:NCIT_C18020",
                                    'operator_attribute': "=",
                                    'attribute': "obo:NCIT_C7057",
                                    'instance': "output_type",
                                    'operator_output': "=",
                                    'output': "obo:OGMS_0000073",
                                    'cde': stamp})                                      
                            queryText = queryText + Block
                                                            
                            with open('templates/block3c_VALUES.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                    'instance': "output_identifier",
                                    'values': curated_values,
                                    'cde':stamp})                                       
                            queryText = queryText + Block
                            queryText = queryText + "}"
                                       
                        else:
                            sys.exit( "DISEASE ({parameter.type}) filter not permitted.")   

            queryText = queryText + "}"       

        else:
            sys.exit("Any of the parameters you passed is not corrected, please check you input JSON request body")
           
        # Debugging 
        
        # stamp_file = "latest_query.ttl"
        # f = open(stamp_file, "a")
        # f.write(queryText)
        # f.close()
                
        result = self.TRIPLE_STORE_CONECTION.get_count_individuals(queryText)
        count = result["results"]["bindings"][0]["count"]["value"]
        return count