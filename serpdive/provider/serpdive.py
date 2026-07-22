from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from serpdive import (
    AuthenticationError,
    InvalidRequestError,
    QuotaExceededError,
    RateLimitError,
    SerpDive,
    SerpDiveError,
)


class SerpdiveProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validates the API key without spending credits: an empty query stops
        at authentication, so a valid key gets HTTP 400 (missing_query) and an
        invalid one gets HTTP 401. No search runs and nothing is billed.
        """
        api_key = credentials.get("serpdive_api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("SERPdive API key is missing.")

        try:
            with SerpDive(api_key=api_key, timeout=15.0, max_retries=0) as client:
                client.search("")
        except AuthenticationError as e:
            raise ToolProviderCredentialValidationError(str(e))
        except InvalidRequestError:
            # The key passed authentication; only the empty query was rejected.
            return
        except (RateLimitError, QuotaExceededError):
            # The key is real; only a usage limit is in the way right now.
            return
        except SerpDiveError as e:
            raise ToolProviderCredentialValidationError(
                f"Could not verify the API key: {e}"
            )
