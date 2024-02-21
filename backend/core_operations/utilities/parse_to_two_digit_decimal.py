from .base import Decimal, InvalidOperation, ROUND_HALF_UP

def parse_to_two_digit_decimal(value):
    try:
        # Attempt to convert and round the value
        if value is not None:
            return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError, TypeError) as e:
        # Log the error, adjust the logging as per your application's logging setup
        print(f"Error formatting decimal value '{value}': {e}")
    # Return None if there's an error or if the input value is None
    return None