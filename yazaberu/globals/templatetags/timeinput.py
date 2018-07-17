from django import template

register = template.Library()

@register.inclusion_tag('globals/timeinput.html')
def timeinput(id, name, value="", default="12:00", takes_context=True):
    return {'id':id, 'name': name, 'value': value, 'default': default}