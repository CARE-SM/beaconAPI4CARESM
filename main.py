from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from beaconObjects import IndividualResponse, Request
from querySelection import QueryBuilder

# URL_SERVER="http://0.0.0.0:8000/"
URL_SERVER = os.getenv("URL_SERVER")

app = FastAPI(
    title="Beacon-API for CARE-SM", version="0.0.8", openapi_url="/openapi.json", openapi_route="/openapi.json") 

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

service = QueryBuilder()

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
async def individuals_counts(input_data: Request):
    try:
        count_result = service.individuals_query_builder(input_data=input_data)
        does_data_exist = count_result is not None
        return IndividualResponse(
            meta={'apiVersion': input_data.meta.apiVersion, 
                  'beaconId': "undefined beacon ID", 
                  'returnedGranularity': "record"},
            responseSummary={
                'numTotalResults': count_result or 0,
                'exists': does_data_exist})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)