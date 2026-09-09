import uuid
import datetime
from decimal import Decimal


def make_json_serializable(value):

    if isinstance(value, uuid.UUID):
        return str(value)

    if isinstance(value, Decimal):
        return str(value)

    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()

    if isinstance(value, dict):
        return {
            key: make_json_serializable(val)
            for key, val in value.items()
        }

    if isinstance(value, (list, tuple, set)):
        return [
            make_json_serializable(item)
            for item in value
        ]

    return value