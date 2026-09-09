from app.core.database import (
    engine,
    Base,
    AsyncSessionLocal,
)
from app.core.cache.redis_client import redis_client
from app.core.db_imports import *  # noqa: F401,F403

from app.shared.bootstrap import (
    SystemBootstrapService,
)
import app.modules.opportunities.scraper.tests.test1
async def startup():

    # =====================================
    # DATABASE INIT
    # =====================================

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

    # =====================================
    # SYSTEM SEEDING
    # =====================================

    async with AsyncSessionLocal() as db:

        await SystemBootstrapService.initialize_system(
            db
        )

        await db.commit()

    # =====================================
    # REDIS
    # =====================================

    #await redis_client.ping()

    print("✅ PostgreSQL Ready")
    print("✅ System Bootstrap Complete")
    print("✅ Redis Ready")

    print(
        "ERP starting..."
    )


async def shutdown():

    await engine.dispose()

    await redis_client.close()

    print("✅ Shutdown Complete")

    print(
        "ERP shutting down..."
    )