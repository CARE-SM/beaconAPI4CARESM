from typing import List
from pydantic import BaseModel, Optional

## Catalog Request:

class CatalogRequestFilter(BaseModel):
    id: str
    operator: str
    value: str

class CatalogMetaContent(BaseModel):
    apiVersion: str

class CatalogRequestQuery(BaseModel):
    filters :List[CatalogRequestFilter]

class CatalogRequest(BaseModel):
    meta: CatalogMetaContent
    query: CatalogRequestQuery

## Catalog Response:

class CatalogsResults(BaseModel):
    id: str
    name: str
    description: str
    externalUrl: str
    resourceTypes: str
    organisation: str

class ResultsetsResponseContent(BaseModel):
    id: str
    setType: str
    exists: bool
    resultsCount: int
    results: List[CatalogsResults]

class CatalogsResponseContent(BaseModel):
    resultSets: List[ResultsetsResponseContent]


class CatalogsResponseSummaryContent(BaseModel):
    exists: bool
    numTotalResults: int


class CatalogsMetaResponseContent(BaseModel):
    apiVersion: str
    beaconId: str
    returnedGranularity: str

class CatalogResponse(BaseModel):
    meta: CatalogsMetaResponseContent
    responseSummary: CatalogsResponseSummaryContent
    response: CatalogsResponseContent


## Individuals Request:

class RequestFilter(BaseModel):
    type: str
    id: str
    operator: str

class RequestQuery(BaseModel):
    filters: List[RequestFilter]

class MetaContent(BaseModel):
    apiVersion: str

class IndividualRequest(BaseModel):
    meta: MetaContent
    query: RequestQuery


## Individual Response:

class IndividualResultSets(BaseModel):
    id: str
    type: str
    exists: bool
    resultCount: int   

class IndividualsResults(BaseModel):
    resultSets: IndividualResultSets ## No very well explained in the Spec


class IndividualResponseContent(BaseModel):
    exists: bool
    numTotalResults: int  

class IndividualsMetaResponseContent(BaseModel):
    apiVersion: str
    beaconId: str
    returnedGranularity: str

class IndividualResponse(BaseModel):
    meta: IndividualsMetaResponseContent
    response: IndividualsResults
    responseSummary: IndividualResponseContent