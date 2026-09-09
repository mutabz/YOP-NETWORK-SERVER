from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.seeders import OpportunitySeeder


class SystemBootstrapService:


    @staticmethod
    async def initialize_system(
        db: AsyncSession
    ):
        #
        # RBAC Permission Catalog
        #

        #await OpportunitySeeder.seed(
        #    db
        #)

        await db.commit()


        return True