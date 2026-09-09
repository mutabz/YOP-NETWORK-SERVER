from datetime import date

from app.shared.data_pipeline.context import SettingsContext
from app.shared.data_pipeline.formatters.date_format import (
    DateFormatFormatter,
)


class DateTransformer:
    """
    Transforms date values according to company settings.

    This transformer handles date formatting only.
    It does not perform timezone conversion.
    """

    @staticmethod
    def format(
        value: date,
        context: SettingsContext,
    ) -> str:
        """
        Format a date using the company's configured
        date format.
        """

        if not isinstance(value, date):
            raise TypeError(
                f"Expected date, got {type(value).__name__}"
            )

        python_format = DateFormatFormatter.to_python(
            context.date_format,
        )

        return value.strftime(python_format)