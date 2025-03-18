# Create a file: issues/templatetags/rating_tags.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    return dictionary.get(key, 0)

@register.filter
def star_range(value):
    """Return a range based on the given value for star ratings"""
    return range(int(value))

@register.filter
def empty_star_range(value):
    """Return a range for the remaining empty stars"""
    if value > 5:
        value = 5
    return range(5 - int(value))