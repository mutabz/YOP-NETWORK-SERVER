from decimal import Decimal, ROUND_HALF_UP

from app.shared.data_pipeline.context.settings_context import SettingsContext
from app.shared.data_pipeline.values.currency_value import CurrencyValue


class CurrencyTransformer:
    """
    Pure currency presentation/transformation utilities.

    Currency conversion itself belongs to CurrencyService.

    This transformer does not:
        - query the database
        - resolve exchange rates
        - resolve currencies
        - modify company settings
    """

    # =========================================================
    # ROUNDING
    # =========================================================

    @staticmethod
    def round(
        value: CurrencyValue,
        decimal_places: int,
    ) -> CurrencyValue:
        """
        Round a monetary value according to currency precision.
        """

        if decimal_places < 0:
            raise ValueError(
                "Decimal places cannot be negative."
            )

        quantizer = Decimal("1").scaleb(
            -decimal_places
        )

        rounded_amount = value.amount.quantize(
            quantizer,
            rounding=ROUND_HALF_UP,
        )

        return CurrencyValue(
            amount=rounded_amount,
            currency=value.currency,
        )

    # =========================================================
    # FORMATTING
    # =========================================================

    @staticmethod
    def format(
        value: CurrencyValue,
        currency,
        *,
        include_symbol: bool = True,
        include_code: bool = False,
    ) -> str:
        """
        Format a monetary value using currency metadata.

        The supplied currency should correspond to
        value.currency.

        Example:

            CurrencyValue(
                amount=Decimal("145000"),
                currency="RWF",
            )

        Result:

            "145,000 FRw"

        With include_code=True:

            "145,000 FRw RWF"
        """

        decimal_places = currency.decimal_places

        quantizer = Decimal("1").scaleb(
            -decimal_places
        )

        amount = value.amount.quantize(
            quantizer,
            rounding=ROUND_HALF_UP,
        )

        formatted_amount = (
            f"{amount:,.{decimal_places}f}"
        )

        parts: list[str] = [
            formatted_amount,
        ]

        if include_symbol and currency.symbol:
            parts.append(currency.symbol)

        if include_code:
            parts.append(currency.code)

        return " ".join(parts)

    # =========================================================
    # COMPANY FORMATTING
    # =========================================================

    @staticmethod
    def format_for_company(
        value: CurrencyValue,
        context: SettingsContext,
        *,
        include_symbol: bool = True,
        include_code: bool = False,
    ) -> str:
        """
        Format a monetary value using the company's
        configured base currency.

        This method does not perform conversion.

        The value should already be in the company's
        currency.

        Example:

            CurrencyValue(
                amount=Decimal("145000"),
                currency="RWF",
            )

        Company currency:

            RWF

        Result:

            "145,000 FRw"
        """

        return CurrencyTransformer.format(
            value=value,
            currency=context.currency,
            include_symbol=include_symbol,
            include_code=include_code,
        )