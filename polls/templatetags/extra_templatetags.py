from django import template

register = template.Library()

@register.filter(name='isinteger')
def isinteger(value):
    if type(value) == int:
        return True
    else:
        return False