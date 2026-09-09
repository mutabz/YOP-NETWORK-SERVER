from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.shared.data_pipeline.context.settings_context import SettingsContext
from app.shared.data_pipeline.formatters.date_format import (
    DateFormatFormatter,
)
from app.shared.data_pipeline.formatters.time_format import (
    TimeFormatFormatter,
)


class DateTimeTransformer:
    """
    Transforms datetime values according to company settings.

    Responsibilities:
        - Convert datetime to company timezone.
        - Apply company date format.
        - Apply company time format.
    """

    @staticmethod
    def format(
        value: datetime,
        context: SettingsContext,
    ) -> str:
        """
        Convert and format a datetime according to
        company settings.
        """

        if not isinstance(value, datetime):
            raise TypeError(
                f"Expected datetime, got {type(value).__name__}"
            )

        localized = DateTimeTransformer._to_company_timezone(
            value,
            context,
        )

        date_format = DateFormatFormatter.to_python(
            context.date_format,
        )

        time_format = TimeFormatFormatter.to_python(
            context.time_format,
        )

        return localized.strftime(
            f"{date_format} {time_format}"
        )

    @staticmethod
    def _to_company_timezone(
        value: datetime,
        context: SettingsContext,
    ) -> datetime:
        """
        Convert a datetime into the company's configured
        timezone.

        Naive datetimes are assumed to be UTC.
        """

        if value.tzinfo is None:
            value = value.replace(
                tzinfo=timezone.utc
            )

        company_timezone = ZoneInfo(
            context.timezone.name
        )

        return value.astimezone(
            company_timezone
        )