class TimeFormatFormatter:
    """
    Converts application time-format tokens into
    Python strftime format tokens.
    """

    FORMATS = {
        "24h": "%H:%M",
        "12h": "%I:%M %p",
    }

    @classmethod
    def to_python(
        cls,
        time_format: str,
    ) -> str:
        """
        Convert an application time format to
        a Python strftime format.

        Supported:

            24h → %H:%M
            12h → %I:%M %p
        """

        if not isinstance(time_format, str):
            raise TypeError(
                "Time format must be a string."
            )

        normalized = time_format.strip().lower()

        if not normalized:
            raise ValueError(
                "Time format cannot be empty."
            )

        try:
            return cls.FORMATS[normalized]
        except KeyError:
            raise ValueError(
                f"Unsupported time format: {time_format}"
            )