# Django imports
from django import template
from django.utils.formats import number_format

register = template.Library()

@register.filter
def number_beautify(value):
    """
    """
    return number_format(int(value), force_grouping=True)

@register.filter
def daily_production(value):
    """
    """
    return value * 24
