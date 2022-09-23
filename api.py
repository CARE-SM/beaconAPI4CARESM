from typing import List
from unicodedata import name
from fastapi import FastAPI
from pydantic import BaseModel
from SPARQLWrapper import SPARQLWrapper2

from config import config as configuration
import chevron


#app = FastAPI()

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




#@app.get("/")
# def apiRunning():
#     return {"message": "API running"} 

#@app.post("/individuals")
def individualsCountingQuery(input_data):  # input_data: Input
    """
    Counting for individuals, creates modular SPARQL queries based on EJP CDE semantic models. Parameters are passed as request body where you define what data elements are you searching for. \n
    Specifications can be found here: https://github.com/ejp-rd-vp/vp-api-specs \n
    It retrieves JSON object that defines counted individuals as {"count" : nº of individuals} \n
    """

    with open('templates/basicTemplate.mustache', 'r') as f:
        queryText = chevron.render(f)

    # Explore all filters that are sent as Request body
    for parameter in input_data["properties"]["query"]["filters"]:

        # In case of Sex filter is called:
        if parameter["types"] == "obo:NCIT_C28421":
            with open('templates/sexTemplate.mustache', 'r') as f:
                sexBlock = chevron.render(f, {'sexReference': parameter["ids"]})

            queryText = queryText + sexBlock

        # In case of Disease filter is called:
        elif parameter["types"] == "sio:SIO_001003":
            with open('templates/diseaseTemplate.mustache', 'r') as f:
                diseaseBlock = chevron.render(f, {'diseaseReference': parameter["ids"]})

            queryText = queryText + diseaseBlock
    queryText = queryText + "\n" + "}" + "\n"

    # Define SPARQL connections based on modular SPARQL query created below:
    sparql = SPARQLWrapper2(configuration["endpoint"]) # Fetch endpoint from other file
    sparql.setQuery(str(queryText))
    countValue = sparql.query().bindings[0]["count"].value
    return {"count": countValue}



data_exemplar = {
    "description": "string",
    "properties": {
      "query": {
        "description": "string",
        "filters": [
          {
            "types": "obo:NCIT_C28421",
            "ids": "obo:NCIT_C16576",
            "operator": "="
          }
        ]
      }
    }
  }

test = individualsCountingQuery(input_data=data_exemplar)
print(test)