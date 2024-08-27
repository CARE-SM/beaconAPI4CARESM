from typing import List, Optional, Union
from pydantic import BaseModel

## Beacon Individual Request

class AlphanumericRequestFilterList(BaseModel):
    id: List[str]
    operator: str
    type: str
    
class AlphanumericRequestFilter(BaseModel):
    id: str
    operator: str
    type: str

class OntologyRequestFilter(BaseModel):
    id: str
    operator: Optional[str] = None
    type: Optional[str] = None

class OntologyRequestFilterList(BaseModel):
    id: List[str]
    operator: Optional[str] = None
    type: Optional[str] = None

    
class RequestQuery(BaseModel):
    filters :List[Union[AlphanumericRequestFilter, OntologyRequestFilter, AlphanumericRequestFilterList, OntologyRequestFilterList]] = []

class ReturnedSchemas(BaseModel):
    entityType: Optional[str] = None
    scheme: Optional[str] = None

class MetaContent(BaseModel):
    apiVersion: str
    beaconID: Optional[str] = None
    returnedSchemas: List[ReturnedSchemas] = None

class IndividualRequest(BaseModel):
    meta: MetaContent
    query: RequestQuery
    
    class Config:
        json_schema_extra = {
            "example": { 
                "meta":{
                    "apiVersion": "v4.0",
                    "returnedSchemas": []
                },
                    "query": {
                        "filters": [
                        {
                            "type": "obo:NCIT_C83164",
                            "id": "1904",
                            "operator": ">="
                        }
                        ]
                    }
                }
        }