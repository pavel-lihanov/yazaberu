from django import template

register = template.Library()

@register.inclusion_tag('globals/calendar.html')
def calendar(id, takes_context=True):
    return {'id': id}