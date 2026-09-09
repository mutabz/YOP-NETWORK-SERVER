from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.system_layer.localization.currency.repositories.currency import (
    CurrencyRepository,
)
from app.modules.system_layer.localization.currency.repositories.exchange_rate import (
    ExchangeRateRepository,
)
from app.modules.system_layer.localization.currency.services.currency import (
    CurrencyService,
)

from app.shared.data_pipeline.context.settings_context import SettingsContext
from app.shared.data_pipeline.transformers import CurrencyTransformer
from app.shared.data_pipeline.values.currency_value import CurrencyValue


class CurrencyResolver:
    """
    Resolves monetary values using the company's configured
    base currency.

    Conversion business logic is delegated to CurrencyService.

    Formatting/presentation is delegated to CurrencyTransformer.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        currency_repository = CurrencyRepository(session)
        exchange_rate_repository = ExchangeRateRepository(session)

        self.currency_service = CurrencyService(
            currency_repository=currency_repository,
            exchange_rate_repository=exchange_rate_repository,
        )

    # =========================================================
    # CONVERSION
    # =========================================================

    async def resolve(
        self,
        value: CurrencyValue,
        context: SettingsContext,
        *,
        as_of: date | None = None,
    ) -> CurrencyValue:
        """
        Convert a monetary value into the company's
        configured base currency.

        Example:

            CurrencyValue(
                amount=Decimal("100"),
                currency="USD",
            )

            Company currency = RWF

            Result:

            CurrencyValue(
                amount=Decimal("145000"),
                currency="RWF",
            )
        """

        converted_amount = await self.currency_service.convert(
            amount=value.amount,
            from_currency=value.currency,
            to_currency=context.currency.code,
            as_of=as_of,
        )

        return CurrencyValue(
            amount=converted_amount,
            currency=context.currency.code,
        )

    # =========================================================
    # FORMATTING
    # =========================================================

    def format_for_company(
        self,
        value: CurrencyValue,
        context: SettingsContext,
        *,
        include_symbol: bool = True,
        include_code: bool = False,
    ) -> str:
        """
        Format a monetary value using the company's
        configured base currency.

        Example:

            CurrencyValue(
                amount=Decimal("145000"),
                currency="RWF",
            )

            →

            "145,000 FRw"
        """

        return CurrencyTransformer.format_for_company(
            value=value,
            context=context,
            include_symbol=include_symbol,
            include_code=include_code,
        )

    # =========================================================
    # CONVERT + FORMAT
    # =========================================================

    async def convert_and_format(
        self,
        value: CurrencyValue,
        context: SettingsContext,
        *,
        as_of: date | None = None,
        include_symbol: bool = True,
        include_code: bool = False,
    ) -> str:
        """
        Convert a monetary value into the company's
        base currency and format the result.

        Example:

            USD 100
                ↓
            exchange rate
                ↓
            RWF 145,000
                ↓
            "145,000 FRw"
        """

        converted = await self.resolve(
            value=value,
            context=context,
            as_of=as_of,
        )

        return self.format_for_company(
            value=converted,
            context=context,
            include_symbol=include_symbol,
            include_code=include_code,
        )