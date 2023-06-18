from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date, datetime
import re


# custom validator 01 - form 
def validate_vehicle_year(value):
    # Check if value is a 4-digit number
    if not isinstance(value, int) or value < 1000 or value > 9999:
        raise ValidationError("The year must be a 4-digit number. Ex: 2022")
    # Check if value is greater than today().year + 1
    if value > date.today().year+1:
        raise ValidationError(f"The year can't be greater than {date.today().year+1}.")

# custom validator 02 
def validate_file_size(value):
    filesize = value.size
    if filesize > 1024 * 1024 * 8:   # 8MB in bytes
        raise ValidationError("The maximum file size that can be uploaded is 8MB.")

# custom validator 03

def validate_phone_number(value):
    value =re.sub(r'\D',value)
    # Check if value has exactly 10 digits. US phone number. no country codde 1, or +1 is needed.
    if not re.match(r'^\d{10}$', value):
        raise ValidationError('Enter a valid 10-digit US phone number.Ex: 2223334444')

# Regular expression pattern for valid zip code
def validate_zip_code(value):
    if not isinstance(value, int):
        raise ValidationError('Zip code must be numbers. Ex. 92844, 92704.')
    else:
        ZIP_CODE_REGEX = r'^\d{5}(?:[-\s]\d{4})?$'
        zip_code_validator = RegexValidator(regex=ZIP_CODE_REGEX, message='Enter a valid ZIP code.')
        return zip_code_validator