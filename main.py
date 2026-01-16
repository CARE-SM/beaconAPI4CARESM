from fastapi import FastAPI, HTTPException, status
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
from datetime import datetime

from models.beaconIndividualRequest import IndividualRequest
from models.beaconIndividualResponse import IndividualResponse
from models.curie import CURIEFiltering
from querySelection import QueryBuilder

# Configuration
URL_SERVER = os.getenv("URL_SERVER", "http://0.0.0.0:8000")
PROXY_PATH = os.getenv("PROXY_PATH", "beacon")

API_TITLE = "Beacon-API for CARE-SM"
API_VERSION = "4.2.0"

logger = logging.getLogger(__name__)

# App initialization
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    openapi_url="/openapi.json",
)

# Enable CORS if needed (safe default)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # tighten in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Service layer (single instance)
query_service = QueryBuilder()

# OpenAPI customization
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        routes=app.routes,
    )
    # Faib requirement
    openapi_schema["servers"] = [{"url": URL_SERVER}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Routes
@app.get("/", tags=["metadata"])
def api_status():
    return {"status": "ok", "service": API_TITLE}

@app.get("/filtering_terms", response_model=CURIEFiltering, tags=["metadata"])
def valid_terms_for_filtering():
    try:
        filters, curie = query_service.filtering_CURIE()
        return CURIEFiltering(
            meta={
                "beaconId": "undefined beacon ID",
                "apiVersion": API_VERSION,
                "returnedSchemas": [],
            },
            response={
                "resources": curie,
                "filteringTerms": filters,
            },
        )
    except Exception as e:
        logger.exception("Failed to get filtering terms")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve filtering terms",
        ) from e

def milisec():
    return datetime.now().strftime('%Y%m%d%H%M%S%f')


def _build_individuals_response(
    count_result: int | None,
    api_version: str,
) -> IndividualResponse:
    exists = bool(count_result and count_result > 0)
    count = count_result or 0

    return IndividualResponse(
        meta={
            "apiVersion": api_version,
            "beaconId": "undefined beacon ID",
            "returnedGranularity": "record",
        },
        response={
            "resultSets": [
                {
                    "id": f"result_{milisec()}",
                    "type": "dataset",
                    "exists": exists,
                    "resultCount": count,
                }
            ]
        },
        responseSummary={
            "numTotalResults": count,
            "exists": exists,
        },
    )

@app.post(f"/{PROXY_PATH}/individuals", response_model=IndividualResponse, tags=["individuals"])
async def individuals_counts(input_data: IndividualRequest):
    try:        
        count_result = query_service.individuals_query_builder(input_data=input_data)

        try:
            count_result = int(count_result)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=500,
                detail="Invalid count value returned from query service"
            )
        return _build_individuals_response(
            count_result=count_result,
            api_version=input_data.meta.apiVersion,
        )
    except ValueError as ve:
        logger.warning("Invalid request: %s", ve)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        ) from ve
    except Exception as e:
        logger.exception("Individuals query failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)# reload=True)