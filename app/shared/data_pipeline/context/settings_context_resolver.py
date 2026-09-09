from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.system_layer.organisation.company_settings.models.company_settings import (
    CompanySettings,
)
from app.modules.system_layer.organisation.company_settings.repositories.company_settings import (
    CompanySettingsRepository,
)
from app.shared.data_pipeline.context.settings_context import SettingsContext
from app.shared.data_pipeline.exceptions import (
    CompanySettingsNotFoundError,
)


class SettingsContextResolver:
    """
    Resolves company settings into an immutable SettingsContext.

    The resolver loads the company's configuration and converts it
    into the immutable context consumed by the data pipeline.

    Responsibilities:

        Company ID
            ↓
        CompanySettingsRepository
            ↓
        CompanySettings
            ↓
        SettingsContext
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.repository = CompanySettingsRepository(session)

    async def resolve(
        self,
        company_id: UUID,
    ) -> SettingsContext:
        """
        Resolve settings for a company.

        Args:
            company_id:
                Company whose settings should be resolved.

        Returns:
            Immutable SettingsContext.

        Raises:
            CompanySettingsNotFoundError:
                If the company has no settings.
        """

        settings: CompanySettings | None = (
            await self.repository.get_by_company_id(
                company_id
            )
        )

        if settings is None:
            raise CompanySettingsNotFoundError(
                company_id=company_id,
            )

        return SettingsContext(
            company_id=settings.company_id,
            currency=settings.base_currency,
            timezone=settings.timezone,
            locale=settings.locale,
            date_format=settings.date_format,
            time_format=settings.time_format,
            fiscal_year_start_month=(
                settings.fiscal_year_start_month
            ),
            fiscal_year_start_day=(
                settings.fiscal_year_start_day
            ),
            tax_inclusive_pricing=(
                settings.tax_inclusive_pricing
            ),
        )