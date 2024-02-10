import re
from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date, datetime
from core_operations.common_functions import format_phone_number_to_shop_standard, deformat_phone_numbers

from core_operations.constants import LIST_OF_STATES_IN_US

# custom validator 01 - vehicle year
def validate_vehicle_year(value):
    # Check if value is a 4-digit number
    if not isinstance(value, int) or value < 1000 or value > 9999:
        raise ValidationError("The year must be a 4-digit number. Ex: 2022")
    # Check if value is greater than today().year + 1
    if value > date.today().year+1:
        raise ValidationError(f"The year can't be greater than {date.today().year+1}.")

# custom validator 02 - file size 8MB
def validate_file_size(value):
    filesize = value.size
    if filesize > 1024 * 1024 * 8:   # 8MB in bytes
        raise ValidationError("The maximum file size that can be uploaded is 8MB.")

# custom validator 03 - phone number
# def validate_phone_number(value):
#     value =re.sub(r'\D',value)
#     # Check if value has exactly 10 digits. US phone number. no country codde 1, or +1 is needed.
#     if not re.match(r'^\d{10}$', value):
#         raise ValidationError('Enter a valid 10-digit US phone number.Ex: 2223334444, or (222)333-4444.')

def validate_phone_number(value):
    # javacript based script will format the user's input as (800)234-0690.
    value = deformat_phone_numbers(value)
    # Check if value has exactly 10 digits. US phone number. no country codde 1, or +1 is needed.
    if not re.match(r'^\d{10}$', value):
        raise ValidationError(
            'The phone number should have 10digits. Ex: 2223334444, or (222)333-4444.')
    
# custom validator 04 - zip_code. Regular expression pattern for valid zip code
def validate_zip_code(value):
    if not isinstance(value, int):
        raise ValidationError('Zip code must be numbers. Ex. 92844, 92704.')
    else:
        ZIP_CODE_REGEX = r'^\d{5}(?:[-\s]\d{4})?$'
        zip_code_validator = RegexValidator(regex=ZIP_CODE_REGEX, message='Enter a valid ZIP code.')
        return zip_code_validator


# custom validator 05 - the list of us states
def validate_us_state(value):
    if value not in dict(LIST_OF_STATES_IN_US):
        raise ValidationError('Invalid US state abbreviation.')

