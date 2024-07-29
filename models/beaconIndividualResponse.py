from typing import List, Optional, Union
from pydantic import BaseModel

## Beacon Individual Response

class IndividualResponseContent(BaseModel):
    exists: bool
    numTotalResults: int 

class IndividualResultSets(BaseModel):
    id: str
    type: str
    exists: bool
    resultCount: int   

class IndividualsResults(BaseModel):
    resultSets: List[IndividualResultSets]
 
class IndividualsMetaResponseContent(BaseModel):
    apiVersion: str
    beaconId: str
    returnedGranularity: str

class IndividualResponse(BaseModel):
    meta: IndividualsMetaResponseContent
    response: IndividualsResults
    responseSummary: IndividualResponseContent