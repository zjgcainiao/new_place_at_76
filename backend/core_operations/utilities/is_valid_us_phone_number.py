from .base import phonenumbers
def is_valid_us_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, 'US')
        return phonenumbers.is_valid_number(parsed_number) or phonenumbers.is_possible_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False
