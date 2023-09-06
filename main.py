from typing import List
from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from querySelection import QuerySelection
import requests
import yaml
# from fastapi.routing import Path




app = FastAPI()
service = QuerySelection()

# Input classes:

class Request(BaseModel):
    id: str

class Filters(BaseModel):
    type: str
    id: str
    operator: str

class Query(BaseModel):
    description: str
    filters: List[Filters]

class Properties(BaseModel):
    query: Query

class Input(BaseModel):
    description: str
    properties: Properties


# Output classes:

class ResponseSummary(BaseModel):
    numTotalResults: int
    exists: bool

class Response(BaseModel):
    responseSummary: ResponseSummary


# Protocols:

@app.get("/")
def apiRunning():
    return {"message": "API running"} 

@app.get("/spec", response_class=JSONResponse)
def spec():
    try:
        response = requests.get("https://raw.githubusercontent.com/ejp-rd-vp/vp-api-specs/main/individuals_api_v0.2.yml")
        yaml_data = yaml.load(response.content)
        return JSONResponse(content=yaml_data)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None        

@app.post("/individuals")
def countingIndividuals(input_data:Input):
    """
    Counting for individuals, creates modular SPARQL queries based on EJP CDE semantic models. Parameters are passed as request body where you define what data elements are you searching for. \n
    Specifications can be found here: https://github.com/ejp-rd-vp/vp-api-specs \n
    It retrieves JSON object that defines counted individuals as {"count" : nº of individuals} \n
    """

    count_result = service.individualsCountingQuery(input_data=input_data)
    does_data_exist = False
    if count_result is not None:
        does_data_exist = True
    else:
        count_result = 0
    return Response(responseSummary={'numTotalResults': count_result, 'exists': does_data_exist})


@app.post('/proxy/{rest_of_path:path}')
async def catalogDiscoverability(input_data:Input, rest_of_path : str = Path(..., description="URL path with forward slashes")):
    # SPARQL builder step:
    sparql_creation = service.catalogCountingQuery(input_data=input_data)
    return {
        "endpoint": rest_of_path,
        "queryString":sparql_creation.queryString}

    # # Proxy POST step
    # endpoint = "http://beaconproxy-sparqler/proxy"
    # json_body = {
    #     "endpoint": rest_of_path,
    #     "queryString":sparql_creation.queryString}

    # proxy_request = requests.post(endpoint, json=json_body)
    # print(proxy_request)

    # return {"response":proxy_request}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)