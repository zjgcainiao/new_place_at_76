from .base import US_COUNTRY_CODE
import re
# common function 08
def format_phone_number_to_shop_standard(phone_number):
    phone_number_digits = re.sub(r'\D', '', phone_number)
    if len(phone_number_digits) == 10:
        full_phone_number_digits = US_COUNTRY_CODE + phone_number_digits
        # Format the phone number as "+1 (818) 223-4456"
        return '+{}({}){}-{}'.format(
            full_phone_number_digits[0:1],
            full_phone_number_digits[1:4],
            full_phone_number_digits[4:7],
            full_phone_number_digits[7:11],
        )
    else:
        raise ValueError('The input must be a 10-digit US phone number.')
