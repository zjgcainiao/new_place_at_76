def validate_decimal(value, max_digits=20, decimal_places=2):
    # validates a input is a no more than 20 digit,2 decimal placed decimal.
    integer_part = int(value)
    decimal_part = value - integer_part
    if len(str(integer_part)) > max_digits - decimal_places or len(str(decimal_part)[2:]) > decimal_places:
        return False
    return True
