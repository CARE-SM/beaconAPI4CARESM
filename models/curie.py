from typing import List, Optional, Union
from pydantic import BaseModel

class CURIEformat(BaseModel):
    id:str
    name:str
    url:str
    version:str
    namespacePrefix:str
    iriPrefix:str

class FilteringTerms(BaseModel):
    id:str
    label:str
    type:str
    scopes: List[str]= None 

class responseFilters(BaseModel):
    resources: List[CURIEformat]
    filteringTerms: List[FilteringTerms]   

class metaFilters(BaseModel):
    apiVersion: str
    beaconId: str
    returnedSchemas: List[str]= None

class CURIEFiltering(BaseModel):
    meta: metaFilters
    response: responseFilters