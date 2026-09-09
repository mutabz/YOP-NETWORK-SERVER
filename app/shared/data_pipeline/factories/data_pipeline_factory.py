from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.data_pipeline.context import (
    SettingsContext,
    SettingsContextResolver,
)
from app.shared.data_pipeline.pipeline import DataPipeline
from app.shared.data_pipeline.resolvers.currency_resolver import (
    CurrencyResolver,
)


class DataPipelineFactory:
    """
    Factory responsible for creating a fully configured
    DataPipeline for a company.

    The factory:

        1. Resolves company settings.
        2. Creates required domain resolvers.
        3. Wires them into DataPipeline.
        4. Returns the pipeline and its context.
    """

    @staticmethod
    async def create(
        session: AsyncSession,
        company_id: UUID,
    ) -> tuple[DataPipeline, SettingsContext]:

        # =====================================================
        # 1. RESOLVE COMPANY SETTINGS
        # =====================================================

        settings_resolver = SettingsContextResolver(
            session=session,
        )

        context = await settings_resolver.resolve(
            company_id=company_id,
        )

        # =====================================================
        # 2. CREATE CURRENCY RESOLVER
        # =====================================================

        currency_resolver = CurrencyResolver(
            session=session,
        )

        # =====================================================
        # 3. CREATE PIPELINE
        # =====================================================

        pipeline = DataPipeline(
            currency_resolver=currency_resolver,
        )

        return pipeline, context