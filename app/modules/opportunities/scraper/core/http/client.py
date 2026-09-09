from collections.abc import Mapping

import httpx

from .exceptions import (
    ConnectionError,
    FetchError,
    HTTPStatusError,
    RequestTimeoutError,
)


class HTTPClient:
    """
    Reusable asynchronous HTTP client for scraper infrastructure.

    Responsibilities:
        - HTTP requests
        - headers
        - timeout
        - status validation
        - basic error translation

    It does not:
        - parse HTML
        - discover sitemap URLs
        - map opportunities
    """

    def __init__(
        self,
        *,
        timeout: float = 30.0,
        headers: Mapping[str, str] | None = None,
        follow_redirects: bool = True,
    ) -> None:
        default_headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(compatible; OpportunityScraper/1.0)"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,*/*;q=0.8"
            ),
        }

        if headers:
            default_headers.update(headers)

        self._client = httpx.AsyncClient(
            timeout=timeout,
            headers=default_headers,
            follow_redirects=follow_redirects,
        )

    async def get(
        self,
        url: str,
    ) -> httpx.Response:
        """
        Perform an asynchronous HTTP GET request.
        """

        try:
            response = await self._client.get(url)

        except httpx.TimeoutException as exc:
            raise RequestTimeoutError(
                f"Request timed out: {url}"
            ) from exc

        except httpx.ConnectError as exc:
            raise ConnectionError(
                f"Could not connect to: {url}"
            ) from exc

        except httpx.HTTPError as exc:
            raise FetchError(
                f"HTTP request failed for: {url}"
            ) from exc

        if response.is_error:
            raise HTTPStatusError(
                status_code=response.status_code,
                url=url,
            )

        return response

    async def get_text(
        self,
        url: str,
    ) -> str:
        """
        Fetch a URL and return its response body as text.
        """

        response = await self.get(url)

        return response.text

    async def close(self) -> None:
        """
        Close the underlying HTTP client.
        """

        await self._client.aclose()

    async def __aenter__(self) -> "HTTPClient":
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        await self.close()