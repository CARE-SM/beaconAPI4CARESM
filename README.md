# Beacon API for CARE-SM patient data 

Beacon API prepared to obtain anonymous counts from [CARE Semantic Model.](https://github.com/CARE-SM/CARE-Semantic-Model)-based patient data registries. This implementation transforms Beacon HTTP POST requests into CARE-SM compatible SPARQL counting queries for patient data information. These counting outcomes are based on the filters defined at the Beacon request. After the execution of these queries, the anonymous counting information is transformed into a Beacon Response and retrieved as API responses.

### Considerations:

This beacon API is meanted to point to a TripleStore repository with CARE-SM-based patient data. The SPARQL query that this implementation creates is only compatible with CARE Semantic Model.

## Documentation:

This implementation follows the [EJPRD Virtual Platform API specifications for Beacon API v.2.0](https://github.com/ejp-rd-vp/vp-api-specs) at Github

## Usage:

If you're using [FAIR-in-a-box](https://github.com/ejp-rd-vp/FiaB) (Fiab) interface to manage your healthcare data, this credential information is already configured at Fiab environmental variables.

## Beacon Request

Exemplar Beacon request with data element filter formatted in JSON:

```json
{ 
  "meta":{
    "apiVersion": "v2.0",
    "returnedSchemas": []

},
    "query": {
         "filters": [
          {
            "type": "obo:NCIT_C124353",
            "id": "7",
            "operator": ">"
          },
          {
            "type": "obo:NCIT_C28421",
            "id": "obo:NCIT_C16576",
            "operator": "="
          },
          {
            "type": "sio:SIO_010056",
            "id": "obo:HP_0003131",
            "operator": "="
          }
        ]
       }
   }
```

## Docker

This whole implementation is Dockerized at Docker hub, check our public image [here](https://hub.docker.com/repository/docker/pabloalarconm/ejprd-counting-api). 

You can run the docker image in a compose file that contains your environmental variables with your credentials, like this:

``` yaml
version: '3'
services:
  api:
    image: pabloalarconm/ejprd-counting-api:0.0.7
    ports:
      - "8000:8000"
    environment:
      - TRIPLESTORE_URL=http://localhost:7200/repositories/exemplar_vp_api_repo
      - TRIPLESTORE_USERNAME=admin
      - TRIPLESTORE_PASSWORD=root

      - FILTER_SEX=True
      - FILTER_DISEASE=True
      - FILTER_SYMPTOM=True
      - FILTER_GENE_VARIANT=True
      - FILTER_BIRTHYEAR=True
      - FILTER_AGE_SYMPTOM_ONSET=True
      - FILTER_AGE_DIAGNOSIS=True

```
