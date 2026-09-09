from sqlalchemy import or_, String, cast
from sqlalchemy.sql.sqltypes import JSON


class SearchBuilder:

    @staticmethod
    def apply(
        query,
        model,
        search: str,
        fields: list
    ):

        if not search:
            return query

        conditions = []

        pattern = f"%{search}%"

        for field in fields:

            if not hasattr(model, field):
                continue

            column = getattr(model, field)

            # =============================================
            # JSON / JSON ARRAY
            # =============================================

            if isinstance(column.type, JSON):

                conditions.append(
                    cast(
                        column,
                        String
                    ).ilike(pattern)
                )

            # =============================================
            # NORMAL STRING/TEXT FIELDS
            # =============================================

            else:

                conditions.append(
                    column.ilike(pattern)
                )

        if conditions:

            query = query.filter(
                or_(*conditions)
            )

        return query