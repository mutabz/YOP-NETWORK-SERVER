from dataclasses import dataclass, field


@dataclass(slots=True)
class ScraperResult:
    source_name: str

    discovered: int = 0
    succeeded: int = 0
    failed: int = 0

    errors: list[str] = field(default_factory=list)

    @property
    def processed(self) -> int:
        return self.succeeded

    def add_success(self) -> None:
        self.succeeded += 1

    def add_error(self, error: Exception | str) -> None:
        self.failed += 1
        self.errors.append(str(error))
