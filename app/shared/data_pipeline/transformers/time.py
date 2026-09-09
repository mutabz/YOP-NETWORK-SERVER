from datetime import time

from app.shared.data_pipeline.context import SettingsContext
from app.shared.data_pipeline.formatters.time_format import (
    TimeFormatFormatter,
)


class TimeTransformer:
    """
    Transforms time values according to company settings.

    This transformer only handles time formatting.
    It does not perform timezone conversion.
    """

    @staticmethod
    def format(
        value: time,
        context: SettingsContext,
    ) -> str:
        """
        Format a time using the company's configured
        time format.
        """

        if not isinstance(value, time):
            raise TypeError(
                f"Expected time, got {type(value).__name__}"
            )

        python_format = TimeFormatFormatter.to_python(
            context.time_format,
        )

        return value.strftime(python_format)