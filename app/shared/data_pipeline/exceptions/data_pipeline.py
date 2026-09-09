from uuid import UUID


class DataPipelineError(Exception):
    """Base exception for data pipeline errors."""


class SettingsResolutionError(DataPipelineError):
    """Base exception for settings resolution errors."""


class CompanySettingsNotFoundError(SettingsResolutionError):
    """Raised when company settings cannot be found."""

    def __init__(self, company_id: UUID) -> None:
        self.company_id = company_id

        super().__init__(
            f"Company settings not found for company: {company_id}"
        )