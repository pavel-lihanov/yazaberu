from django import template
import datetime
register = template.Library()

@register.inclusion_tag('globals/calendar.html')
def calendar(id, value="", takes_context=True):
    #print(value, type(value))
    if value:
        return {'id': id, 'value': value.isoformat()}
    else:
        return {'id': id, 'value': ''}