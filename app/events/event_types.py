from enum import Enum


class EventType(str, Enum):

    # USERS
    USER_CREATED = "users.created"
    USER_UPDATED = "users.updated"
    USER_DELETED = "users.deleted"

    # HR
    EMPLOYEE_CREATED = "employee.created"
    EMPLOYEE_UPDATED = "employee.updated"

    # PAYROLL
    PAYROLL_PROCESSED = "payroll.processed"

    # INVENTORY
    STOCK_UPDATED = "stock.updated"

    # MAINTENANCE
    WORK_ORDER_CREATED = "workorder.created"

    # NOTIFICATIONS
    DOCUMENT_GENERATE = "document.create"
    DOCUMENT_GENERATED = "document.created"

    NOTIFICATION_CREATED = "notification.created"
    EMAIL_SEND_REQUESTED = "email.send.requested"
    EMAIL_SEND = "email.send"
    SMS_SEND = "sms.send"

    # CACHE
    CACHE_INVALIDATE = "cache.invalidate"

    # AUDIT
    AUDIT_LOG = "audit.log"

    # REPORTS
    REPORT_GENERATED = "report.generated"

    # REALTIME
    WEBSOCKET_EMIT = "websocket.emit"

    PAYMENT_CREATED = "payment.created"
    PAYMENT_PENDING = "payment.pending"
    PAYMENT_SUCCESS = "payment.success"
    PAYMENT_FAILED = "payment.failed"
    PAYMENT_CANCELLED = "payment.cancelled"
    PAYMENT_REFUNDED = "payment.refunded"
    PAYMENT_WEBHOOK_RECEIVED = "payment.webhook.received"

    INVITATION_ACCEPTED = "invitation.accepted"
    # INVOICE_
    INVOICE_CREATED = "invoice.created"

    INVOICE_PAID = "invoice.paid"

    SUBSCRIPTION_INVOICE_PAID = "invoice.subscription.paid"
    LICENSING_INVOICE_PAID = "invoice.licensing.paid"
    SALES_INVOICE_PAID = "invoice.sales.paid"