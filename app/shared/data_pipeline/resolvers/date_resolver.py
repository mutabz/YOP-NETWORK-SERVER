from datetime import date

from app.shared.data_pipeline.context.settings_context import SettingsContext
from app.shared.data_pipeline.transformers import (
    DateTransformer,
)


class DateResolver:
    """
    Resolves date values using company settings.
    """

    @staticmethod
    def resolve(
        value: date,
        context: SettingsContext,
    ) -> str:
        return DateTransformer.format(
            value=value,
            context=context,
        )