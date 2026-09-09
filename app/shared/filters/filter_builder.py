from sqlalchemy import and_


class FilterBuilder:

    @staticmethod
    def apply(stmt, model, filters: dict):

        if not filters:
            return stmt

        conditions = []

        for raw_field, value in filters.items():

            if value is None:
                continue

            field_name, operator = FilterBuilder._parse_field(raw_field)
            column = getattr(model, field_name, None)

            if column is None:
                continue

            condition = FilterBuilder._build_condition(column, operator, value)
            if condition is not None:
                conditions.append(condition)

        return stmt.where(and_(*conditions)) if conditions else stmt

    @staticmethod
    def _parse_field(raw_field: str):
        if "__" in raw_field:
            field_name, operator = raw_field.rsplit("__", 1)
            return field_name, operator.lower()

        return raw_field, "eq"

    @staticmethod
    def _build_condition(column, operator: str, value):
        if operator in {"eq", "exact"}:
            return column == value

        if operator in {"ne", "not"}:
            return column != value

        if operator == "gt":
            return column > value

        if operator == "gte":
            return column >= value

        if operator == "lt":
            return column < value

        if operator == "lte":
            return column <= value

        if operator == "in":
            return column.in_(value)

        if operator == "notin":
            return column.notin_(value)

        if operator == "contains":
            return column.contains(value)

        if operator == "icontains":
            return column.ilike(f"%{value}%")

        if operator == "startswith":
            return column.startswith(value)

        if operator == "endswith":
            return column.endswith(value)

        if operator == "isnull":
            return column.is_(None) if value else column.is_not(None)

        return column == value