from enum import Enum


class EmailTemplateCode(str, Enum):

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    WELCOME_USER = "WELCOME_USER"

    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"

    PASSWORD_RESET = "PASSWORD_RESET"

    PASSWORD_CHANGED = "PASSWORD_CHANGED"

    ACCOUNT_ACTIVATED = "ACCOUNT_ACTIVATED"

    ACCOUNT_DEACTIVATED = "ACCOUNT_DEACTIVATED"


    # =========================================================
    # SYSTEM
    # =========================================================

    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"


    # =========================================================
    # BUSINESS
    # =========================================================

    INVOICE_CREATED = "INVOICE_CREATED"

    INVOICE_SENT = "INVOICE_SENT"

    INVOICE_PAID = "INVOICE_PAID"

    INVOICE_OVERDUE = "INVOICE_OVERDUE"


    # =========================================================
    # PAYMENTS
    # =========================================================

    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"

    PAYMENT_FAILED = "PAYMENT_FAILED"

    PAYMENT_REFUNDED = "PAYMENT_REFUNDED"