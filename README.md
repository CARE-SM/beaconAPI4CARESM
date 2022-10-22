# Counting Individual API for EJP-RD Virtual Platform 

REST API prepared to obtain anonymous patient counts from FAIRified data registries.


## Documentation:

This implementations follows our Virtual Platform API specifications at our Github repository: https://github.com/ejp-rd-vp/vp-api-specs

## Usage:

This API communication requires a configuration file where credentials and endpoint are specified:

```yaml

# Example:
TRIPLESTORE_URL: http://localhost:7200/repositories/vp_api_repo # And example of a GraphDB Triplestore endpoint
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
        "filters": [ // You can add multiple filters among all parameters documented above
          {
            "types": "obo:NCIT_C28421",  // filter for Sex patient information
            "ids": "obo:NCIT_C16576",  // OBO term for Female
            "operator": "="
          },{
            "types": "sio:SIO_001003", // filter for disease patient information
            "ids": "ordo:Orphanet_1398", // Orphanet code for disease
            "operator": "="
          }
        ]
      }
    }
  }

```

## Docker

You can also build our Docker Image for this API. First you have to edit our [config.yaml]() with your credentials and then you can your Docker Image by:

``` bash
cd ejprd-counting-vp-api

docker -t build ejprd-counting-vp-api .

docker run --network="host" -p 8000:8000 --name ejprd-counting-vp-api ejprd-counting-vp-api
```

## Considerations:

Your endpoint MUST point to a FAIRified Triplestore that contains RDF data aligned with [EJP-RD Common Data Element Semantic Model](https://github.com/ejp-rd-vp/CDE-semantic-model)