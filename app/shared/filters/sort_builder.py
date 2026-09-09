from sqlalchemy import asc, desc


class SortBuilder:

    @staticmethod
    def apply(stmt, model, sort_by: str = None, direction: str = "asc"):

        column = getattr(model, sort_by, None)

        if column is None:
            return stmt

        if direction.lower() == "desc":
            return stmt.order_by(desc(column))

        return stmt.order_by(asc(column))