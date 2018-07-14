from django import template

register = template.Library()

@register.inclusion_tag('globals/edit.html')
def edit(id, value="", _class="", placeholder="", name=None, label=None, container_class="", show_calendar=False, calendar_d=None, url=""):
    print(calendar_d)
    return {
        'id': id, 
        'class': _class, 
        'value': value, 
        'placeholder': placeholder, 
        'name': name if name else id,
        'label': label,
        'container_class': container_class,
        'calendar_d': calendar_d,
        'show_calendar': show_calendar,
        'url': url
        }