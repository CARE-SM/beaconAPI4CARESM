from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
import uvicorn
import requests
import yaml

from beaconObjects import * 
from querySelection import QueryBuilder

app = FastAPI(
    title="Beacon API")

service = QueryBuilder()

@app.get("/")
def api_status():
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