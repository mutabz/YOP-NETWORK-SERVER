from abc import ABC, abstractmethod


class BaseFetcher(ABC):
    """
    Base contract for fetching content from external sources.

    A fetcher is responsible only for retrieving content.
    It does not parse or map the content.
    """

    name: str

    def __init__(
        self,
        *,
        config: dict | None = None,
    ) -> None:
        self.config = config or {}

    @abstractmethod
    async def fetch(
        self,
        url: str,
    ) -> str:
        """
        Fetch content from a URL.

        Args:
            url: Resource URL.

        Returns:
            Raw response content.
        """
        raise NotImplementedError