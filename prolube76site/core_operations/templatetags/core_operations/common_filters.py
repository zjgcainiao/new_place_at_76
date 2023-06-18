from django import template

register = template.Library()

@register.filter
def format_phone_number_to_shop_standard(value):
    return f"({value[:3]}){value[3:6]}-{value[6:]}"


@register.filter
def length(value):
    return len(value) if value else 0