from enum import Enum

class EmailStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    SENDING = "SENDING"
    SENT = "SENT"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class EmailType(str, Enum):
    TRANSACTIONAL = "TRANSACTIONAL"
    NOTIFICATION = "NOTIFICATION"
    SYSTEM = "SYSTEM"
    MARKETING = "MARKETING"

class EmailPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"

class EmailRecipientType(str, Enum):
    TO = "TO"
    CC = "CC"
    BCC = "BCC"

class EmailSourceModule(str, Enum):

    # =========================================================
    # CORE / SYSTEM
    # =========================================================

    SYSTEM = "SYSTEM"

    AUTH = "AUTH"

    NOTIFICATION = "NOTIFICATION"

    # =========================================================
    # BUSINESS
    # =========================================================

    ACCOUNTING = "ACCOUNTING"
    FINANCE = "FINANCE"

    SALES = "SALES"

    PURCHASE = "PURCHASE"

    INVENTORY = "INVENTORY"

    # =========================================================
    # PEOPLE / CUSTOMER
    # =========================================================

    HR = "HR"

    CRM = "CRM"

    # =========================================================
    # FINANCE / PAYMENTS
    # =========================================================

    PAYMENTS = "PAYMENTS"

    # =========================================================
    # REPORTING
    # =========================================================

    REPORTING = "REPORTING"

    # =========================================================
    # COMMUNICATION
    # =========================================================

    MARKETING = "MARKETING"

    # =========================================================
    # INTEGRATIONS
    # =========================================================

    INTEGRATION = "INTEGRATION"

class EmailProvider(str, Enum):
    SMTP = "SMTP"
    GMAIL = "GMAIL"
    OUTLOOK = "OUTLOOK"
    SENDGRID = "SENDGRID"
    MAILGUN = "MAILGUN"

class EmailSendJobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

