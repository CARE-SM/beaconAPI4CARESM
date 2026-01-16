from SPARQLWrapper import SPARQLWrapper, JSON, POST, BASIC
import logging
import os
from typing import Dict, Any


logger = logging.getLogger(__name__)


class TripleStoreConnection:
    """
    Small wrapper around SPARQLWrapper for querying a triplestore.
    """

    def __init__(
        self,
        endpoint_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: int = 60,
    ):
        # Prefer environment variables, allow explicit override
        self.endpoint_url = endpoint_url or os.getenv("TRIPLESTORE_URL")
        self.username = username or os.getenv("TRIPLESTORE_USERNAME")
        self.password = password or os.getenv("TRIPLESTORE_PASSWORD")
        self.timeout = timeout

        self._validate_config()

    def _validate_config(self) -> None:
        """Fail fast if configuration is invalid."""
        missing = [
            name
            for name, value in {
                "TRIPLESTORE_URL": self.endpoint_url,
                "TRIPLESTORE_USERNAME": self.username,
                "TRIPLESTORE_PASSWORD": self.password,
            }.items()
            if not value
        ]

        if missing:
            raise RuntimeError(
                f"Missing required triplestore configuration: {', '.join(missing)}"
            )

        if not self.endpoint_url.startswith(("http://", "https://")):
            raise RuntimeError("TRIPLESTORE_URL must be a valid HTTP(S) URL")

    def get_count_individuals(self, query: str) -> Dict[str, Any]:
        """
        Execute a SPARQL query and return the raw JSON result.
        """
        if not isinstance(query, str) or not query.strip():
            raise ValueError("SPARQL query must be a non-empty string")

        logger.debug("Executing SPARQL query")
        logger.debug(query)

        try:
            endpoint = SPARQLWrapper(self.endpoint_url)
            endpoint.setHTTPAuth(BASIC)
            endpoint.setCredentials(self.username, self.password)
            endpoint.setMethod(POST)
            endpoint.setReturnFormat(JSON)
            endpoint.setTimeout(self.timeout)
            endpoint.setQuery(query)

            result = endpoint.query().convert()

            self._validate_result(result)
            return result

        except Exception as e:
            logger.exception("SPARQL endpoint query failed")
            raise RuntimeError("SPARQL endpoint query failed") from e

    @staticmethod
    def _validate_result(result: Dict[str, Any]) -> None:
        """Basic sanity check on SPARQL JSON result."""
        if not isinstance(result, dict):
            raise RuntimeError("Invalid SPARQL response: not a JSON object")

        if "results" not in result or "bindings" not in result["results"]:
            raise RuntimeError("Invalid SPARQL response: missing results/bindings")
