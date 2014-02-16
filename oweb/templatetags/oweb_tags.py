"""These tags are used to enhance the templates"""
# Django imports
from django import template
from django.utils.formats import number_format

register = template.Library()

@register.filter
def number_beautify(value):
    """Inserts seperators into large numbers"""
    return number_format(int(value), force_grouping=True)

@register.filter
def daily_production(value):
    """Calculates the production in 24 hours"""
    return value * 24
