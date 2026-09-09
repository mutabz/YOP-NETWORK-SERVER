from enum import Enum


class RealtimeEvent(str, Enum):

    # ==========================
    # SYSTEM
    # ==========================

    CONNECTED = "system.connected"
    DISCONNECTED = "system.disconnected"

    PING = "system.ping"
    PONG = "system.pong"

    # ==========================
    # NOTIFICATIONS
    # ==========================

    NOTIFICATION_CREATED = "notification.created"
    NOTIFICATION_READ = "notification.read"
    NOTIFICATION_DELETED = "notification.deleted"

    # ==========================
    # DASHBOARD
    # ==========================

    DASHBOARD_REFRESH = "dashboard.refresh"

    # ==========================
    # CHAT
    # ==========================

    CHAT_MESSAGE = "chat.message"

    # ==========================
    # INVENTORY
    # ==========================

    STOCK_UPDATED = "inventory.stock.updated"

    # ==========================
    # ACCOUNTING
    # ==========================

    INVOICE_CREATED = "invoice.created"
    INVOICE_PAID = "invoice.paid"