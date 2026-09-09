from datetime import date, datetime, time
from typing import Any

from app.shared.data_pipeline.context.settings_context import SettingsContext
from app.shared.data_pipeline.resolvers.currency_resolver import (
    CurrencyResolver,
)
from app.shared.data_pipeline.resolvers.date_resolver import DateResolver
from app.shared.data_pipeline.resolvers.datetime_resolver import (
    DateTimeResolver,
)
from app.shared.data_pipeline.resolvers.time_resolver import TimeResolver
from app.shared.data_pipeline.values.currency_value import CurrencyValue


class DataPipeline:
    """
    Central pipeline for applying company settings to data.

    General transformation supports:

        - datetime
        - date
        - time

    Currency operations are handled explicitly through
    dedicated currency methods because conversion may
    require database access and exchange-rate resolution.
    """

    def __init__(
        self,
        currency_resolver: CurrencyResolver,
    ) -> None:
        self.currency_resolver = currency_resolver

    # =========================================================
    # GENERAL TRANSFORMATION
    # =========================================================

    async def transform(
        self,
        value: Any,
        context: SettingsContext,
    ) -> Any:
        """
        Transform automatically supported values according
        to company settings.

        Supported:

            datetime → formatted datetime
            date     → formatted date
            time     → formatted time

        Unsupported values are returned unchanged.

        CurrencyValue is intentionally NOT handled here.
        """

        if value is None:
            return None

        # datetime must be checked before date because
        # datetime is a subclass of date.
        if isinstance(value, datetime):
            return DateTimeResolver.resolve(
                value=value,
                context=context,
            )

        if isinstance(value, date):
            return DateResolver.resolve(
                value=value,
                context=context,
            )

        if isinstance(value, time):
            return TimeResolver.resolve(
                value=value,
                context=context,
            )

        return value

    # =========================================================
    # CURRENCY RESOLUTION
    # =========================================================

    async def resolve_currency(
        self,
        value: CurrencyValue,
        context: SettingsContext,
        *,
        as_of: date | None = None,
    ) -> CurrencyValue:

        return await self.currency_resolver.resolve(
            value=value,
            context=context,
            as_of=as_of,
        )

    # =========================================================
    # CURRENCY FORMATTING
    # =========================================================

    async def format_currency(
        self,
        value: CurrencyValue,
        context: SettingsContext,
        *,
        include_symbol: bool = True,
        include_code: bool = False,
    ) -> str:

        return await self.currency_resolver.format_for_company(
            value=value,
            context=context,
            include_symbol=include_symbol,
            include_code=include_code,
        )

    # =========================================================
    # CURRENCY CONVERSION + FORMATTING
    # =========================================================

    async def convert_and_format_currency(
        self,
        value: CurrencyValue,
        context: SettingsContext,
        *,
        as_of: date | None = None,
        include_symbol: bool = True,
        include_code: bool = False,
    ) -> str:

        return await self.currency_resolver.convert_and_format(
            value=value,
            context=context,
            as_of=as_of,
            include_symbol=include_symbol,
            include_code=include_code,
        )

    # =========================================================
    # CURRENCY TRANSFORMATION
    # =========================================================

    async def transform_currency(
        self,
        value: Any,
        currency: str,
        context: SettingsContext,
        *,
        as_of: date | None = None,
        include_symbol: bool = True,
        include_code: bool = False,
    ) -> str:

        currency_value = CurrencyValue(
            amount=value,
            currency=currency,
        )

        return await self.convert_and_format_currency(
            value=currency_value,
            context=context,
            as_of=as_of,
            include_symbol=include_symbol,
            include_code=include_code,
        )