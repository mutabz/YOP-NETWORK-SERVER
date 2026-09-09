from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class CurrencyValue:
    """
    Represents a monetary value together with its currency.

    This is a pure pipeline value object.

    It does not:
        - query the database
        - resolve exchange rates
        - know company settings
        - format itself

    Currency is represented by its ISO-style currency code,
    for example:

        USD
        EUR
        RWF
    """

    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        # Normalize monetary amount to Decimal.
        object.__setattr__(
            self,
            "amount",
            Decimal(str(self.amount)),
        )

        # Normalize currency code.
        normalized_currency = str(
            self.currency
        ).strip().upper()

        if not normalized_currency:
            raise ValueError(
                "Currency code cannot be empty."
            )

        object.__setattr__(
            self,
            "currency",
            normalized_currency,
        )