from django import template

register = template.Library()

@register.inclusion_tag('globals/calendar.html')
def calendar(takes_context=True):
    return {}