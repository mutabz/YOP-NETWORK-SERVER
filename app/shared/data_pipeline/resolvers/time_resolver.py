from datetime import time

from app.shared.data_pipeline.context.settings_context import SettingsContext
from app.shared.data_pipeline.transformers import (
    TimeTransformer,
)


class TimeResolver:
    """
    Resolves time values using company settings.
    """

    @staticmethod
    def resolve(
        value: time,
        context: SettingsContext,
    ) -> str:
        return TimeTransformer.format(
            value=value,
            context=context,
        )