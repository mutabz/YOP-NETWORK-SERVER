from app.modules.opportunities.scraper.core.bases.fetcher import (
    BaseFetcher,
)
from app.modules.opportunities.scraper.core.http.client import (
    HTTPClient,
)


class HTTPFetcher(BaseFetcher):
    """
    Fetcher implementation backed by HTTPClient.

    Responsible only for retrieving remote content.
    """

    name = "http"

    def __init__(
        self,
        *,
        client: HTTPClient,
        config: dict | None = None,
    ) -> None:
        super().__init__(config=config)
        self.client = client

    async def fetch(
        self,
        url: str,
    ) -> str:
        """
        Fetch a URL and return its response body.
        """

        return await self.client.get_text(url)