class DateFormatFormatter:
    """
    Converts application date-format tokens into
    Python strftime format tokens.

    Example:

        DD/MM/YYYY
        ↓
        %d/%m/%Y
    """

    TOKENS = {
        "YYYY": "%Y",
        "YY": "%y",
        "MM": "%m",
        "DD": "%d",
    }

    @classmethod
    def to_python(
        cls,
        date_format: str,
    ) -> str:
        """
        Convert an application date format to
        a Python strftime format.
        """

        if not isinstance(date_format, str):
            raise TypeError(
                "Date format must be a string."
            )

        normalized = date_format.strip()

        if not normalized:
            raise ValueError(
                "Date format cannot be empty."
            )

        result = normalized

        for token, replacement in cls.TOKENS.items():
            result = result.replace(
                token,
                replacement,
            )

        return result