from math import ceil
from sqlalchemy import func, select


class Paginator:

    @staticmethod
    async def paginate(session, stmt, page: int = 1, per_page: int = 20):

        page = max(page, 1)
        per_page = max(per_page, 1)

        # optimized count (no full fetch)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await session.scalar(count_stmt)

        # pagination
        stmt = stmt.offset((page - 1) * per_page).limit(per_page)

        result = await session.execute(stmt)
        items = result.scalars().all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": ceil(total / per_page) if total else 1
        }