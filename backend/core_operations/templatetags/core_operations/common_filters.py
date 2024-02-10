from django import template
from django.utils.safestring import mark_safe
import re
from dateutil import parser

register = template.Library()


@register.filter
def format_phone_number_to_shop_standard(value):
    phone_number_digits = re.sub(r'\D', '', value)
    return f"({phone_number_digits[:3]}){phone_number_digits[3:6]}-{phone_number_digits[6:]}"


@register.filter
def length(value):
    return len(value) if value else 0


@register.filter(name='bold_last_six_digit_in_vin')
def bold_last_six_digit_in_vin(vin):
    if not vin:
        return ""

    # Bold the last 6 characters
    bold_part = vin[-6:]
    normal_part = vin[:-6]

    return mark_safe(f"{normal_part}<strong>{bold_part}</strong>")

# check a User model's type CustomerUser or InternalUser


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='format_datetime')
def format_datetime(value, format_string="Y-m-d H:i"):
    try:
        # Parse the datetime string to a datetime object
        datetime_obj = parser.parse(value)
        # Format the datetime object
        return format(datetime_obj, format_string)
    except (ValueError, TypeError):
        # Return the original value if parsing fails
        return value