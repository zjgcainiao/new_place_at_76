
from .base import Decimal, InvalidOperation

def convert_to_decimal(value_str, default=None):
    # Convert a string to an integer. If it's empty or not valid, return the default value."""
    try:
        return Decimal(str(value_str))
    # This handles both empty strings and other invalid values
    except (ValueError, TypeError, InvalidOperation):
        return default

