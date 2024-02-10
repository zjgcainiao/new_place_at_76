# In your templatetags directory, create a file custom_filters.py
from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='is_instance_of')
def is_instance_of(value, arg):
    model_class = globals().get(arg)
    return isinstance(value, model_class)
