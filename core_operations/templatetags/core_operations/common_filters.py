from django import template
from django.utils.safestring import mark_safe
import re

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
