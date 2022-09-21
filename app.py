from typing import List
from unicodedata import name
from fastapi import FastAPI
from pydantic import BaseModel
from SPARQLWrapper import SPARQLWrapper2

from config import config as configuration


app = FastAPI()

# POST request body definition: Nested Model

class Filters(BaseModel):
    types: str
    ids: str
    operator: str

class Query(BaseModel):
    description: str
    filters: List[Filters]

class Properties(BaseModel):
    query: Query

class Input(BaseModel):
    description: str
    properties: Properties




@app.get("/")
def apiRunning():
    return {"message": "API running"}

@app.post("/individuals")
def individualsCountingQuery(input_data: Input):
    """
    Counting for individuals, creates modular SPARQL queries based on EJP CDE semantic models. Parameters are passed as request body where you define what data elements are you searching for. \n
    Specifications can be found here: https://github.com/ejp-rd-vp/vp-api-specs \n
    It retrieves JSON object that defines counted individuals as {"count" : nº of individuals} \n
    """

    queryText = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX this: <http://my_example.com/>
PREFIX ordo: <http://www.orpha.net/ORDO/>

SELECT (count(DISTINCT ?id) as ?count)
WHERE {
?id a sio:SIO_000115 .
?entity a sio:SIO_000498 .

"""
    # Explore all filters that are sent as Request body
    for parameter in input_data.properties.query.filters:

        # In case of Sex filter is called:
        if parameter.types == "obo:NCIT_C28421":
            sexBlock = """
?sexrole a sio:SIO_000016 .
?sexrole a obo:OBI_0000093 .
?id sio:SIO_000020 ?sexrole .
?entity sio:SIO_000228 ?sexrole .
?entity sio:SIO_000008 ?sexattribute .

?sexattribute a obo:NCIT_C28421 .
?sexattribute a ?sexuri .
FILTER (?sexuri = {}) . """.format(parameter.ids)

            queryText = queryText + sexBlock

        # In case of Disease filter is called:
        elif parameter.types == "sio:SIO_001003":
            diseaseBlock = """
?diagnosis_role a sio:SIO_000016 .
?diagnosis_role a obo:OBI_0000093 .
?id sio:SIO_000020 ?diagnosis_role .
?entity sio:SIO_000228 ?diagnosis_role .
?entity sio:SIO_000008 ?diagnosis_attribute .

?diagnosis_attribute a ?diagnosis .
FILTER (?diagnosis = {}) . """.format(parameter.ids)

            queryText = queryText + diseaseBlock
    queryText = queryText + "\n" + "}" + "\n"

    # Define SPARQL connections based on modular SPARQL query created below:
    sparql = SPARQLWrapper2(configuration["endpoint"]) # Fetch endpoint from other file
    sparql.setQuery(str(queryText))
    countValue = sparql.query().bindings[0]["count"].value
    return {"count": countValue}