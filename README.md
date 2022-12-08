# Counting Individual API for EJP-RD Virtual Platform 

REST API prepared to obtain anonymous patient counts from FAIRified data registries.


## Documentation:

This implementations follows our Virtual Platform API specifications at our Github repository: https://github.com/ejp-rd-vp/vp-api-specs

## Usage:

This API communication requires a configuration file where credentials and endpoint are specified:

```yaml

# Example:
TRIPLESTORE_URL: http://localhost:7200/repositories/exemplar_vp_api_repo # And example of a GraphDB Triplestore endpoint
TRIPLESTORE_USERNAME: admin
TRIPLESTORE_PASSWORD: root
```

Also, it consumes a JSON object as a HTTP POST Request body with all filters:

Exemplar JSON:

```json
{
    "description": "string",
    "properties": {
      "query": {
        "description": "string",
        "filters": [
          {
            "type": "obo:NCIT_C28421",
            "id": "obo:NCIT_C16576",
            "operator": "="
          },{
            "type": "sio:SIO_010056",
            "id": "obo:HP_0002633",
            "operator": "="
          },{
            "type": "obo:NCIT_C2991",
            "id": "ordo:Orphanet_88918",
            "operator": "="
          }
        ]
      }
    }
  }
```

## Docker

You can also use Docker-based implementation. First, pull the latest [image](https://hub.docker.com/repository/docker/pabloalarconm/ejprd-counting-api). Then you can create a docker compose file that contains your enviromental variables with your credentials, like this:

``` yaml
services:
  api:
    image: pabloalarconm/ejprd-counting-api:0.0.2
    ports:
      - "8000:8000"
    environment:
      - TRIPLESTORE_URL=http://localhost:7200/repositories/exemplar_vp_api_repo
      - TRIPLESTORE_USERNAME=admin
      - TRIPLESTORE_PASSWORD=root

```

## Considerations:

Your endpoint MUST point to a FAIRified Triplestore that contains RDF data aligned with [EJP-RD Common Data Element Semantic Model](https://github.com/ejp-rd-vp/CDE-semantic-model)