class ScraperHTTPError(Exception):
    """
    Base exception for scraper HTTP errors.
    """


class FetchError(ScraperHTTPError):
    """
    Raised when a resource cannot be fetched.
    """


class HTTPStatusError(ScraperHTTPError):
    """
    Raised when the remote server returns an unsuccessful status.
    """

    def __init__(
        self,
        *,
        status_code: int,
        url: str,
        message: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.url = url

        super().__init__(
            message
            or f"HTTP {status_code} returned for {url}"
        )


class RequestTimeoutError(FetchError):
    """
    Raised when an HTTP request times out.
    """


class ConnectionError(FetchError):
    """
    Raised when a connection cannot be established.
    """