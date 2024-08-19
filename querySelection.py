import triplestoreConection
import chevron
from perseo.main import milisec
import sys
import os

class QueryBuilder:

    TRIPLE_STORE_CONECTION = triplestoreConection.TripleStoreConection()
    
    # FILTER_SEX= "True"
    # FILTER_DISEASE= "True"
    # FILTER_SYMPTOM= "True"
    # FILTER_GENE_VARIANT= "True"
    # FILTER_BIRTHYEAR= "True"
    # FILTER_AGE_SYMPTOM_ONSET= "True"
    # FILTER_AGE_DIAGNOSIS= "True"
        
    FILTER_SEX = os.getenv("FILTER_SEX")
    FILTER_DISEASE = os.getenv("FILTER_DISEASE")
    FILTER_SYMPTOM = os.getenv("FILTER_SYMPTOM")
    FILTER_GENE_VARIANT = os.getenv("FILTER_GENE_VARIANT")
    FILTER_BIRTHYEAR = os.getenv("FILTER_BIRTHYEAR")
    FILTER_AGE_SYMPTOM_ONSET = os.getenv("FILTER_AGE_SYMPTOM_ONSET")
    FILTER_AGE_DIAGNOSIS = os.getenv("FILTER_AGE_DIAGNOSIS")
    
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
        except ValueError:
            sys.exit("You can't add non numerical nor fractional years to the filters related to Age, like AGE OF SYMPTOM ONSET and AGE OF DIAGNOSIS")
    
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
            symp_info = {}
            onset_info = {}
            
            # Store parameter.types to for later validation
            for parameter in input_data.query.filters:
                if parameter.type:
                    list_filters_used += [parameter.type]
           
            for parameter in input_data.query.filters:                
                if parameter.type:
                    
                    # SEX FILTER
                    if parameter.type == "obo:NCIT_C28421" or parameter.type =="http://purl.obolibrary.org/obo/NCIT_C28421":
                        if self.FILTER_SEX == "True":
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                    'process': "sio:SIO_000006",
                                    'operator_target': "=",
                                    'target': "sio:SIO_000015",
                                    'operator_attribute': parameter.operator,
                                    'attribute':parameter.id,
                                    'operator_output': "=",
                                    'output': "obo:NCIT_C160908",
                                    'cde':"sex"})
                            queryText = queryText + Block
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"sex"})
                            queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for SEX is not available")

                    # DISEASE FILTER
                    elif parameter.type == "obo:NCIT_C2991" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C2991":
                        if self.FILTER_DISEASE == "True":
                            stamp = "disease" + milisec()

                            if isinstance(parameter.id, str):
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "sio:SIO_000006",
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': parameter.operator,
                                        'attribute':parameter.id,
                                        'operator_output': "=",
                                        'output': "obo:NCIT_C154625",
                                        'cde':stamp})  
                                queryText = queryText + Block

                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id, tag="ont")

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "sio:SIO_000006",
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': "!=",
                                        'attribute': "sio:SIO_000614",
                                        'operator_output': "=",
                                        'output': "obo:NCIT_C154625",
                                        'cde':stamp})                                       
                                queryText = queryText + Block
                                                                
                                with open('templates/block4_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "attribute_type",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block
                                
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':stamp})
                            queryText = queryText + Block
                            
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for DISEASE is not available")

                    # PHENOTYPE FILTER
                    elif ("sio:SIO_010056" in list_filters_used or "http://semanticscience.org/resource/SIO_010056" in list_filters_used) and ("obo:NCIT_C124353" not in list_filters_used and "http://purl.obolibrary.org/obo/NCIT_C124353" not in list_filters_used):
                        if self.FILTER_SYMPTOM == "True":
                            stamp = "phenotype" + milisec()

                            if isinstance(parameter.id, str):
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "sio:SIO_000006",
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': parameter.operator,
                                        'attribute': parameter.id,
                                        'operator_output': "=",
                                        'output': "sio:SIO_000015",
                                        'cde':stamp}) 
                                queryText = queryText + Block
                                                                       
                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id, tag="ont")

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "sio:SIO_000006",
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': "!=",
                                        'attribute': "sio:SIO_000614",
                                        'operator_output': "=",
                                        'output': "sio:SIO_000015",
                                        'cde':stamp})     
                                queryText = queryText + Block
                                    
                                with open('templates/block4_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "attribute_type",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block      
                                    
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':stamp})
                            queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for SYMPTOM/PHENOTYPE is not available")
                        
                    # GENOTYPE FILTER
                    elif parameter.type == "edam:data_2295": 
                        if self.FILTER_GENE_VARIANT == "True":
                            stamp = "genotype" + milisec()
                            
                            if isinstance(parameter.id, str):
                                curated_values = self.curate_values(parameter.id, tag="lit")

                                with open('templates/block4_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "value",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block 

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "obo:NCIT_C15709",
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': "=",
                                        'attribute': "sio:SIO_000614",
                                        'operator_output': "=",
                                        'output': "sio:SIO_000015",
                                        'cde':stamp})
                                queryText = queryText + Block
                                
                                with open('templates/block2b_OUTPUT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':stamp})
                                queryText = queryText + Block
                                
                                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':stamp})
                                queryText = queryText + Block
                                
                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id, tag="lit")
                                
                                with open('templates/block4_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "attribute_type",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "obo:NCIT_C15709",
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': "=",
                                        'attribute': "sio:SIO_000614",
                                        'operator_output': "=",
                                        'output': "sio:SIO_000015",
                                        'cde':stamp})                                                                        
                                queryText = queryText + Block 
                                
                                with open('templates/block2b_OUTPUT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':stamp})
                                queryText = queryText + Block
                                
                                with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                    Block = chevron.render(f, {'cde':stamp})
                                queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for GENETIC VARIANT is not available")

                    # BIRTHYEAR FILTER
                    elif parameter.type == "obo:NCIT_C83164" or parameter.type == "http://purl.obolibrary.org/obo/NCIT_C83164":
                        if self.FILTER_BIRTHYEAR == "True":
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "sio:SIO_000006",
                                            'operator_target': "=",
                                            'target': "sio:SIO_000015",
                                            'operator_attribute': "=",
                                            'attribute': parameter.type,
                                            'operator_output': "=",
                                            'output': "sio:SIO_000015",
                                            'cde':"birthyear"})                                                                        
                            queryText = queryText + Block
                            with open('templates/block3b_OUTPUT_VALUE.mustache', 'r') as f:
                                Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator, 'datatype':"xsd:integer", 'cde':"birthyear"})
                            queryText = queryText + Block
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"birthyear"})
                            queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for BIRTHYEAR is not available")
                        
                    # AGE_OF_SYMPTOM FILTER
                    elif ("sio:SIO_010056" not in list_filters_used and "http://semanticscience.org/resource/SIO_010056" not in list_filters_used) and ("obo:NCIT_C124353" in list_filters_used or "http://purl.obolibrary.org/obo/NCIT_C124353" in list_filters_used):
                        if self.FILTER_AGE_SYMPTOM_ONSET == "True":
                            
                            parameter_checked = self.detect_number_type(parameter.id)
                            
                            with open('templates/block1b_BIND.mustache', 'r') as f:
                                Block = chevron.render(f, {'value': parameter_checked, 'operator': parameter.operator ,'st':"s_",'cde':"s_onset", "cde2":"s_birthdate"})
                            queryText = queryText + Block
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "sio:SIO_000006",
                                            'operator_target': "=",
                                            'target': "sio:SIO_000015",
                                            'operator_attribute': "=",
                                            'attribute': "obo:NCIT_C68615",
                                            'operator_output': "=",
                                            'output': "sio:SIO_000015",
                                            'cde':"s_birthdate"})   
                            queryText = queryText + Block
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"s_birthdate"})
                            queryText = queryText + Block
                            with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"s_birthdate"})
                            queryText = queryText + Block
                            
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "sio:SIO_000006",
                                            'operator_target': "=",
                                            'target': "sio:SIO_000015",
                                            'operator_attribute': "=",
                                            'attribute': "obo:NCIT_C124353",
                                            'operator_output': "=",
                                            'output': "sio:SIO_000015",
                                            'cde':"s_onset"})  
                            queryText = queryText + Block           
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"s_onset"})
                            queryText = queryText + Block
                            with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"s_onset"})
                            queryText = queryText + Block
                            with open('templates/block6_CLOSE.mustache', 'r') as f:
                                Block = chevron.render(f, {})
                            queryText = queryText + Block
                            with open('templates/block6_CLOSE.mustache', 'r') as f:
                                Block = chevron.render(f, {})
                            queryText = queryText + Block
                        else:
                            sys.exit( "You have used unpermitted filter for this repository, filter for AGE OF SYMPTOM ONSET is not available")

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
                                            'operator_target': "=",
                                            'target': "sio:SIO_000015",
                                            'operator_attribute': "=",
                                            'attribute': "obo:NCIT_C68615",
                                            'operator_output': "=",
                                            'output': "sio:SIO_000015",
                                            'cde':"d_birthdate"})                                                                         
                            queryText = queryText + Block
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"d_birthdate"})
                            queryText = queryText + Block
                            with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"d_birthdate"})
                            queryText = queryText + Block
                                                        
                            with open('templates/block2_GENERAL.mustache', 'r') as f:
                                Block = chevron.render(f, {
                                            'process': "sio:SIO_000006",
                                            'operator_target': "=",
                                            'target': "sio:SIO_000015",
                                            'operator_attribute': "=",
                                            'attribute': "sio:SIO_000614",
                                            'operator_output': "=",
                                            'output': "obo:NCIT_C154625",
                                            'cde':"d_onset"})  
                            queryText = queryText + Block
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"d_onset"})
                            queryText = queryText + Block
                            with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':"d_onset"})
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
                    # DISEASE FILTER
                    if self.FILTER_DISEASE == "True":
                        if self.FILTER_DISEASE == "True":
                            stamp = "disease" + milisec()

                            if isinstance(parameter.id, str):
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "sio:SIO_000006",
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': "=",
                                        'attribute':parameter.id,
                                        'operator_output': "=",
                                        'output': "obo:NCIT_C154625",
                                        'cde':stamp})  
                                queryText = queryText + Block
                                   
                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id, tag="ont")

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'process': "sio:SIO_000006",
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': "!=",
                                        'attribute': "sio:SIO_000614",
                                        'operator_output': "=",
                                        'output': "obo:NCIT_C154625",
                                        'cde':stamp})                                       
                                queryText = queryText + Block
                                                                
                                with open('templates/block4_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "attribute_type",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block
                                
                            with open('templates/block5_CONTEXT.mustache', 'r') as f:
                                Block = chevron.render(f, {'cde':stamp})
                            queryText = queryText + Block
                    else:
                        sys.exit( "You have used unpermitted filter for this repository, filter for DISEASE is not available")   

            # SYMPTOM + SYMPTOM ONSET FILTER
            if ("sio:SIO_010056" in list_filters_used or "http://semanticscience.org/resource/SIO_010056" in list_filters_used) and ("obo:NCIT_C124353" in list_filters_used or "http://purl.obolibrary.org/obo/NCIT_C124353" in list_filters_used):
                if (self.FILTER_SYMPTOM == "True") and (self.FILTER_AGE_SYMPTOM_ONSET == "True"):
                    for parameter in input_data.query.filters:
                        if parameter.type =="sio:SIO_010056" or parameter.type =="http://semanticscience.org/resource/SIO_010056":
                            symp_info = parameter

                        elif parameter.type == "obo:NCIT_C124353" or parameter.type =="http://purl.obolibrary.org/obo/NCIT_C124353":
                            onset_info = parameter        
                                
                    parameter_checked = self.detect_number_type(onset_info.id)
                            
                    # SYMPTOM + SYMPTOM ONSET FILTER
                    with open('templates/block1b_BIND.mustache', 'r') as f:
                        Block = chevron.render(f, {'value': onset_info.id, 'operator': onset_info.operator , 'st':"s_", 'cde':"s_onset", "cde2":"s_birthdate"})
                    queryText = queryText + Block
                    with open('templates/block2_GENERAL.mustache', 'r') as f:
                        Block = chevron.render(f, {
                                    'process': "sio:SIO_000006",
                                    'operator_target': "=",
                                    'target': "sio:SIO_000015",
                                    'operator_attribute': "=",
                                    'attribute': "obo:NCIT_C68615",
                                    'operator_output': "=",
                                    'output': "sio:SIO_000015",
                                    'cde':"s_birthdate"})  
                    queryText = queryText + Block
                    with open('templates/block5_CONTEXT.mustache', 'r') as f:
                        Block = chevron.render(f, {'cde':"s_birthdate"})
                    queryText = queryText + Block
                    with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                        Block = chevron.render(f, {'cde':"s_birthdate"})
                    queryText = queryText + Block

                    if isinstance(symp_info.id, str):
                        with open('templates/block2_GENERAL.mustache', 'r') as f:                    
                            Block = chevron.render(f, {
                                'process': "sio:SIO_000006",
                                'operator_target': symp_info.operator,
                                'target': symp_info.id,
                                'operator_attribute': "=",
                                'attribute': "obo:NCIT_C124353",
                                'operator_output': "=",
                                'output': "sio:SIO_000015",
                                'cde':"s_onset"})  
                        queryText = queryText + Block
     
                    elif isinstance(symp_info.id, list):
                        
                        curated_values = self.curate_values(symp_info.id)

                        with open('templates/block2_GENERAL.mustache', 'r') as f:                    
                            Block = chevron.render(f, {
                                'process': "sio:SIO_000006",
                                'operator_target': "!=",
                                'target': "sio:SIO_000015",
                                'operator_attribute': "=",
                                'attribute': "obo:NCIT_C124353",
                                'operator_output': "=",
                                'output': "sio:SIO_000015",
                                'cde':"s_onset"})                         
                        queryText = queryText + Block   
                           
                        with open('templates/block4_VALUES.mustache', 'r') as f:
                            Block = chevron.render(f, {
                                'instance': "target_type",
                                'values': curated_values,
                                'cde':"s_onset"})                                       
                        queryText = queryText + Block      

                    with open('templates/block5_CONTEXT.mustache', 'r') as f:
                        Block = chevron.render(f, {'cde':"s_onset"})
                    queryText = queryText + Block
                    with open('templates/block5b_CONTEXT_DATE.mustache', 'r') as f:
                        Block = chevron.render(f, {'cde':"s_onset"})
                    queryText = queryText + Block
                    with open('templates/block6_CLOSE.mustache', 'r') as f:
                        Block = chevron.render(f, {})
                    queryText = queryText + Block
                    with open('templates/block6_CLOSE.mustache', 'r') as f:
                        Block = chevron.render(f, {})
                    queryText = queryText + Block        
                else:
                    sys.exit( "You have used unpermitted filter for this repository, neither SYMPTOM nor AGE OF SYMPTOM ONSET is available")

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