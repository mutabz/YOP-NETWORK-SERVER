from datetime import datetime

from app.shared.data_pipeline.context.settings_context import SettingsContext
from app.shared.data_pipeline.transformers import (
    DateTimeTransformer,
)


class DateTimeResolver:
    """
    Resolves datetime values using company settings.

    Handles:
        - company timezone
        - company date format
        - company time format
    """

    @staticmethod
    def resolve(
        value: datetime,
        context: SettingsContext,
    ) -> str:
        return DateTimeTransformer.format(
            value=value,
            context=context,
        )