from django import template

register = template.Library()

@register.inclusion_tag('globals/calendar.html')
def calendar(id, value="", takes_context=True):
    print(value, type(value))
    return {'id': id, 'value': value.isoformat()}