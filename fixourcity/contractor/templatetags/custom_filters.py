# contractor/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    try:
        return value * float(arg)
    except (ValueError, TypeError):
        return value  # Return the original value if multiplication fails