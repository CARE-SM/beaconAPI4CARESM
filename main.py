from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from perseo.main import milisec

from models.beaconIndividualRequest import IndividualRequest
from models.beaconIndividualResponse import IndividualResponse
from models.curie import CURIEFiltering

from querySelection import QueryBuilder

# URL_SERVER="http://0.0.0.0:8000/"
# proxy_path="somepath"
URL_SERVER = os.getenv("URL_SERVER")
proxy_path =os.getenv("PROXY_PATH")

app = FastAPI(
    title="Beacon-API for CARE-SM", version="4.0.1", openapi_url="/openapi.json", openapi_route="/openapi.json") 

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins, but you can specify a list of allowed origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods
#     allow_headers=["*"],  # Allow all headers
# )
service = QueryBuilder()

def custom_openapi():
    openapi_schema = get_openapi(title="Beacon-API for CARE-SM ", version="4.0.0", routes=app.routes)
    openapi_schema["servers"] = [{"url": URL_SERVER}]
    return openapi_schema

app.openapi = custom_openapi

@app.get("/")
def api_ejstatus():
    return {"message": "API running"}

@app.get("/filtering_terms")
def valid_terms_for_filtering():
    try:
        filters, curie = service.filtering_CURIE()
        return CURIEFiltering(
            meta={
                'beaconId': "undefined beacon ID", 
                'apiVersion': "v4.0", 
                'returnedSchemas': []
            },
            response={
                'resources': curie,
                'filteringTerms': filters
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/individuals")
async def individuals_counts(input_data: IndividualRequest):
    try:
        count_result = service.individuals_query_builder(input_data=input_data)
        does_data_exist = count_result is not None
        output_data=IndividualResponse(
            meta={
                'apiVersion': input_data.meta.apiVersion, 
                'beaconId': "undefined beacon ID", 
                'returnedGranularity': "record"
                },
            response= {
                    'resultSets': [{
                        'id': "result_" + milisec(),
                        'type': "dataset",
                        'exists': does_data_exist,
                        'resultCount': count_result or 0
                    }]
                },
            responseSummary={
                'numTotalResults': count_result or 0,
                'exists': does_data_exist})
        return output_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post(f"/{proxy_path}/individuals/")
async def individuals_counts(input_data: IndividualRequest):
    try:
        count_result = service.individuals_query_builder(input_data=input_data)
        does_data_exist = count_result is not None
        output_data = IndividualResponse(
            meta={
                'apiVersion': input_data.meta.apiVersion, 
                'beaconId': "undefined beacon ID", 
                'returnedGranularity': "record"
                },
            response= {
                    'resultSets': [{
                        'id': "result_" + milisec(),
                        'type': "dataset",
                        'exists': does_data_exist,
                        'resultCount': count_result or 0
                    }]
                },
            responseSummary={
                'numTotalResults': count_result or 0,
                'exists': does_data_exist})
        return output_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)