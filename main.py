from fastapi import FastAPI #, Path
# from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import uvicorn
# import requests
# import yaml
import os

from beaconObjects import * 
from querySelection import QueryBuilder

app = FastAPI(
    title="Beacon-API for CARE-SM", version="0.0.8", openapi_url="/openapi.json", openapi_route="/openapi.json") 

service = QueryBuilder()
# URL_SERVER="http://0.0.0.0:8000/"
URL_SERVER = os.getenv("URL_SERVER")

def custom_openapi():
    openapi_schema = get_openapi(title="Beacon-API for CARE-SM ", version="0.0.8", routes=app.routes)
    openapi_schema["servers"] = [{"url": URL_SERVER}]
    return openapi_schema

app.openapi = custom_openapi

@app.get("/")
def api_ejstatus():
    return {"message": "API running"}

@app.get("/filtering_terms")
def valid_terms():
    ask_filters = service.filters()
    return ask_filters

@app.post("/individuals")
async def individuals_counts(input_data:Request):

    count_result = service.individuals_query_builder(input_data=input_data)

    does_data_exist = False
    if count_result is not None:
        does_data_exist = True
    else:
        count_result = 0

    return IndividualResponse(
        meta={
            'apiVersion': input_data.meta.apiVersion, 
            'beaconId': "undefined beacon ID", #TODO try to pass beaconId from the request
            'returnedGranularity': "record"},
        responseSummary={
            'numTotalResults': count_result,
            'exists': does_data_exist})

# @app.post('/proxy/{rest_of_path:path}')
# async def catalogDiscoverability(input_data:Request, rest_of_path : str = Path(..., description="URL path with forward slashes")):
#     # SPARQL builder step:
#     sparql_creation = service.catalog_query_builder(input_data=input_data)
#     return {
#         "endpoint": rest_of_path,
#         "queryString":sparql_creation.queryString}

    # # Proxy POST step
    # endpoint = "http://beaconproxy-sparqler/proxy"
    # json_body = {
    #     "endpoint": rest_of_path,
    #     "queryString":sparql_creation.queryString}

    # proxy_request = requests.post(endpoint, json=json_body)
    # print(proxy_request)

    # return {"response":proxy_request}

# @app.post('/catalogs')
# async def catalog_discoverability(input_data:Request):
#     count_result = service.catalog_query_builder(input_data=input_data)

#     does_data_exist = False
#     if count_result[0] != 0:
#         does_data_exist = True

#     return CatalogResponse(
#         meta={
#             'apiVersion': input_data.meta.apiVersion, 
#             'beaconId': "undefined beacon ID", #TODO try to pass beaconId from the request
#             'returnedGranularity': "record"},
#         response = count_result[1],
#         responseSummary={
#             'id': "undefined resultset ID",
#             'setType': "undefined set type",
#             'exists': does_data_exist,
#             'numTotalResults': count_result[0]
#             })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)