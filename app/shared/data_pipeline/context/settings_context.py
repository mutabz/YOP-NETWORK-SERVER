from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.modules.system_layer.localization.currency.models import Currency
    from app.modules.system_layer.localization.locale.models import Locale
    from app.modules.system_layer.localization.timezone.models import Timezone


@dataclass(frozen=True, slots=True)
class SettingsContext:
    """
    Resolved company settings used by the data pipeline.

    This context contains the settings required to transform,
    format, and interpret ERP data for a specific company.

    The context is immutable so that pipeline transformations
    cannot accidentally modify company configuration.
    """

    # =========================================================
    # COMPANY
    # =========================================================

    company_id: UUID

    # =========================================================
    # LOCALIZATION
    # =========================================================

    currency: "Currency"
    timezone: "Timezone"
    locale: "Locale"

    # =========================================================
    # DATE / TIME FORMATTING
    # =========================================================

    date_format: str
    time_format: str

    # =========================================================
    # FISCAL YEAR
    # =========================================================

    fiscal_year_start_month: int
    fiscal_year_start_day: int

    # =========================================================
    # TAX
    # =========================================================

    tax_inclusive_pricing: bool