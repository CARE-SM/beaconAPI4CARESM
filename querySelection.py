import triplestoreConection
import chevron
from perseo.main import milisec
import sys
import os
# from ageCalculation import AgeCalculation

class QueryBuilder:

    TRIPLE_STORE_CONECTION = triplestoreConection.TripleStoreConection()
    permitted_terms = []
    
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
    
    if FILTER_SEX == "True":
        permitted_terms.append("FILTER_SEX")    
    if FILTER_DISEASE == "True":
        permitted_terms.append("FILTER_DISEASE")
    if FILTER_SYMPTOM == "True":
        permitted_terms.append("FILTER_SYMPTOM")
    if FILTER_GENE_VARIANT == "True":
        permitted_terms.append("FILTER_GENE_VARIANT")
    if FILTER_BIRTHYEAR == "True":
        permitted_terms.append("FILTER_BIRTHYEAR")
    if FILTER_AGE_SYMPTOM_ONSET == "True":
        permitted_terms.append("FILTER_AGE_SYMPTOM_ONSET")
    if FILTER_AGE_DIAGNOSIS == "True":
        permitted_terms.append("FILTER_AGE_DIAGNOSIS")
    
    def filters(self):
        return {"permitted_terms": self.permitted_terms} 
    
    def detect_number_type(self, string):
        try:
            # Try converting to integer
            int_value = int(string)
            return int_value
        except ValueError:
            sys.exit("You can't add non numerical nor fractional years to the filters related to Age, like AGE OF SYMPTOM ONSET and AGE OF DIAGNOSIS")
    
    def curate_values(self, values):
        curated_values = ""
        for value in values:
            curated_values += value + " "
        return curated_values
    
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
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': parameter.operator,
                                        'attribute':parameter.id,
                                        'operator_output': "=",
                                        'output': "obo:NCIT_C154625",
                                        'cde':stamp})  
                                    
                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id)

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
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
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': parameter.operator,
                                        'attribute': parameter.id,
                                        'operator_output': "=",
                                        'output': "sio:SIO_000015",
                                        'cde':stamp}) 
                                                                       
                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id)

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': "!=",
                                        'attribute': "sio:SIO_000614",
                                        'operator_output': "=",
                                        'output': "sio:SIO_000015",
                                        'cde':stamp})     
                                    
                                with open('templates/block4_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "attribute_type",
                                        'values': curated_values,
                                        'cde':stamp})                                       
                                queryText = queryText + Block      
                                    
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
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'operator_target': "=",
                                        'target': "obo:NCIT_C45766",
                                        'operator_attribute': "!=",
                                        'attribute': "obo:NCIT_C181350",
                                        'operator_output': "=",
                                        'output': "sio:SIO_000015",
                                        'cde':stamp})
                                queryText = queryText + Block
                                    
                                with open('templates/block3a_TARGET_ID.mustache', 'r') as f:
                                    Block = chevron.render(f, {'value': parameter.id, 'cde':stamp})
                                queryText = queryText + Block
                                                                    
                            elif isinstance(parameter.id, list):
                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'operator_target': "=",
                                        'target': "obo:NCIT_C45766",
                                        'operator_attribute': "!=",
                                        'attribute': "obo:NCIT_C181350",
                                        'operator_output': "=",
                                        'output': "sio:SIO_000015",
                                        'cde':stamp})                                                                        
                                queryText = queryText + Block
                                     
                                with open('templates/block4_VALUES.mustache', 'r') as f:
                                    Block = chevron.render(f, {
                                        'instance': "target_id",
                                        'values': curated_values,
                                        'cde':stamp})                                       
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
                                            'operator_target': "=",
                                            'target': "sio:SIO_000015",
                                            'operator_attribute': "=",
                                            'attribute': parameter.type,
                                            'operator_output': "=",
                                            'output': "sio:SIO_000015",
                                            'cde':"birthyear"})                                                                        
                            queryText = queryText + Block
                            with open('templates/block3b_OUTPUT_VALUE.mustache', 'r') as f:
                                # startage, endage = AgeCalculation.calculateAgeRange(parameter.id, parameter.operator)
                                Block = chevron.render(f, {'value': parameter.id, 'operator': parameter.operator, 'cde':"birthyear"})
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
                                        'operator_target': "=",
                                        'target': "sio:SIO_000015",
                                        'operator_attribute': "=",
                                        'attribute':parameter.id,
                                        'operator_output': "=",
                                        'output': "obo:NCIT_C154625",
                                        'cde':stamp})  
                                    
                            elif isinstance(parameter.id, list):
                                curated_values = self.curate_values(parameter.id)

                                with open('templates/block2_GENERAL.mustache', 'r') as f:
                                    Block = chevron.render(f, {
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
                                'operator_target': symp_info.operator,
                                'target': symp_info.id,
                                'operator_attribute': "=",
                                'attribute': "obo:NCIT_C124353",
                                'operator_output': "=",
                                'output': "sio:SIO_000015",
                                'cde':"s_onset"})  
                            
                    elif isinstance(symp_info.id, list):
                        
                        curated_values = self.curate_values(symp_info.id)

                        with open('templates/block2_GENERAL.mustache', 'r') as f:                    
                            Block = chevron.render(f, {
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