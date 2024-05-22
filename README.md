# Beacon API for CARE-SM patient data 

Beacon API for [CARE Semantic Model.](https://github.com/CARE-SM/CARE-Semantic-Model) to perform anonymous patient counts from data registries. This implementation converts Beacon Requests into CARE-SM SPARQL counting query, retrieving a Beacon-compliant JSON Response with the anonymous outcome.

**Considerations:**

Beacon-API4CARE-SM is only compatible with Triplestore repositories that contain CARE-Semantic Model patient data. 

## Documentation:

This implementation follows the [EJPRD Virtual Platform API specifications for Beacon API v.2.0](https://github.com/ejp-rd-vp/vp-api-specs) at Github.


## API essential paths:
``/openapi.json``: Get the current OpenAPI specification (HTTP GET)

``/filtering_terms``: Get available filters for your counting query (HTTP GET)

``/individuals``: Define metadata and filters for your counting query (HTTP POST)

Exemplar Beacon JSON complaint request containing filter. For more examples, please check your [exemplar_body](/exemplar_body/) folder.

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

## Installation

This whole implementation is Dockerized at Docker hub, check our public image [here](https://hub.docker.com/repository/docker/pabloalarconm/beacon-api4care-sm/). Feel free to implement our docker image next to your TripleStore with CARE-SM patient data.

This beacon API consumes environmental variables for all required parameters related to triplestore credentials (endpoint/username/password) and all available filters to query.

You can run the docker image in a `docker-compose` file that contains your environmental variables with your credentials, like this:

``` yaml
version: '3'
services:
  api:
    image: pabloalarconm/beacon-api4care-sm:0.2.2
    ports:
      - "8000:8000"
    environment:
      - TRIPLESTORE_URL=http://localhost:7200/repositories/exemplar_vp_api_repo
      - TRIPLESTORE_USERNAME=admin
      - TRIPLESTORE_PASSWORD=root
      - URL_SERVER=http://0.0.0.0:8000/

      - FILTER_SEX=True
      - FILTER_DISEASE=True
      - FILTER_SYMPTOM=True
      - FILTER_GENE_VARIANT=True
      - FILTER_BIRTHYEAR=True
      - FILTER_AGE_SYMPTOM_ONSET=True
      - FILTER_AGE_DIAGNOSIS=True

```

This beacon-API4CARE-SM is already deployed at [FAIR-in-a-box](https://github.com/ejp-rd-vp/FiaB) (Fiab) interface.


