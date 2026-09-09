import unittest

from sqlalchemy import Boolean, Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base

from app.shared.filters.filter_builder import FilterBuilder
from app.shared.query_engine import QueryEngine
from app.modules.system_layer.users.repositories.users import UserRepository


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    is_active = Column(Boolean)


class FilterBuilderTests(unittest.TestCase):
    def test_supports_operator_syntax(self):
        stmt = select(User)
        stmt = FilterBuilder.apply(
            stmt,
            User,
            {
                "email__contains": "test",
                "id__in": [1, 2],
                "is_active": True,
            },
        )

        compiled = str(stmt)
        self.assertIn("LIKE", compiled.upper())
        self.assertIn("IN", compiled.upper())


class QueryEngineTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///:memory:")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        self.session = AsyncSession(self.engine, expire_on_commit=False)
        self.query_engine = QueryEngine(self.session, User, None, None, None)

    async def asyncTearDown(self):
        await self.session.close()
        await self.engine.dispose()

    async def test_first_ignores_unknown_select_fields(self):
        user = User(email="test@example.com", is_active=True)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        result = await self.query_engine.first(select_fields=["id", "email", "missing_field"])

        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], user.id)
        self.assertEqual(result["email"], user.email)
        self.assertNotIn("missing_field", result)

    async def test_get_uses_safe_projection_for_repo_usage(self):
        user = User(email="test@example.com", is_active=True)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        result = await self.query_engine.get(user.id, select_fields=["id", "email", "missing_field"])

        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], user.id)
        self.assertEqual(result["email"], user.email)
        self.assertNotIn("missing_field", result)

    async def test_user_repository_get_by_id_returns_the_requested_user(self):
        first_user = User(email="first@example.com", is_active=True)
        second_user = User(email="second@example.com", is_active=True)
        self.session.add_all([first_user, second_user])
        await self.session.commit()
        await self.session.refresh(first_user)
        await self.session.refresh(second_user)

        repo = UserRepository(self.session)
        result = await repo.get_by_id(str(second_user.id), select_fields=["id", "email"])

        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], second_user.id)
        self.assertEqual(result["email"], second_user.email)


if __name__ == "__main__":
    unittest.main()
