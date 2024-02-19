# custom validator 01

from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from django.utils.translation import gettext_lazy as _
from datetime import date, datetime
from core_operations.common_functions import format_phone_number_to_shop_standard, deformat_phone_numbers
import re

# custom validator 01

def validate_vehicle_year(value):
    # Check if value is a 4-digit number
    if not isinstance(value, int) or value < 1000 or value > 9999:
        raise ValidationError("The year must be a 4-digit number. Ex: 2022")
    # Check if value is greater than today().year + 1
    if value > date.today().year+1:
        raise ValidationError(
            f"The year can't be greater than {date.today().year+1}.")

# custom validator 02


def validate_file_size(value):
    filesize = value.size
    if filesize > 1024 * 1024 * 8:   # 8MB in bytes
        raise ValidationError(
            "The maximum file size that can be uploaded is 8MB.")

# custom validator 03


def validate_phone_number(value):
    # javacript based script will format the user's input as (800)234-0690.
    value = deformat_phone_numbers(value)
    # Check if value has exactly 10 digits. US phone number. no country codde 1, or +1 is needed.
    if not re.match(r'^\d{10}$', value):
        raise ValidationError(
            'The phone number should have 10digits. Ex: 2223334444, or (222)333-4444.')


def validate_numeric(value):
    # First, ensure the value is a string; if not, convert it to string for processing
    if not isinstance(value, str):
        value = str(value)
    
    try:
        # Now attempt to convert the stripped value to a decimal
        value = value.strip()
        value = Decimal(value)
    except (ValueError, InvalidOperation):
        # Raise a validation error if conversion fails
        raise ValidationError(_('Enter a valid number.'), code='invalid')