from typing import List, Optional, Union
from pydantic import BaseModel

## Beacon Request, same for /catalog and /individuals

class AlphanumericRequestFilter(BaseModel):
    type: str
    operator: str
    id: str

class OntologyRequestFilter(BaseModel):
    id: str
    operator: Optional[str] = None
    type: Optional[str] = None

class RequestQuery(BaseModel):
    filters :List[Union[AlphanumericRequestFilter, OntologyRequestFilter]] = []

# class ReturnedSchemas(BaseModel):
#     entityType: Optional[str] = None
#     scheme: Optional[str] = None

class MetaContent(BaseModel):
    apiVersion: str
    # beaconID: Optional[str] = None
    # returnedSchemas: List[ReturnedSchemas] = None NO longer a requirement

class Request(BaseModel):
    meta: MetaContent
    query: RequestQuery

## Catalog Response:

# class CatalogsResults(BaseModel): #TODO Beacon have added v3.0 as well.
#     # id: str
#     name: str
#     description: str
#     # externalUrl: str
#     resourceTypes: str
#     # organisation: str

# class ResultsetsResponseContent(BaseModel):
#     id: str
#     setType: str
#     exists: bool
#     resultsCount: int
#     results: List[CatalogsResults]

# class CatalogsResponseContent(BaseModel):
#     resultSets: List[ResultsetsResponseContent]


# class CatalogsResponseSummaryContent(BaseModel):
#     exists: bool
#     numTotalResults: int

# class CatalogsMetaResponseContent(BaseModel):
#     apiVersion: str
#     beaconId: str
#     returnedGranularity: str
#     returnedSchemas: Optional[ReturnedSchemas] = None
    
# class CatalogResponse(BaseModel):
#     meta: CatalogsMetaResponseContent
#     responseSummary: CatalogsResponseSummaryContent
#     response: CatalogsResponseContent

## Individual Response:

class IndividualResponseContent(BaseModel):
    exists: bool
    numTotalResults: int 

# class IndividualResultSets(BaseModel):
#     id: str
#     type: str
#     exists: bool
#     resultCount: int   

# class IndividualsResults(BaseModel):
#     resultSets: List[IndividualResultSets] ## No very well explained in the Spec
 
class IndividualsMetaResponseContent(BaseModel):
    apiVersion: str
    beaconId: str
    returnedGranularity: str

class IndividualResponse(BaseModel):
    meta: IndividualsMetaResponseContent
    #response: IndividualsResults # Blocked due to security outcome, only counts.
    responseSummary: IndividualResponseContent