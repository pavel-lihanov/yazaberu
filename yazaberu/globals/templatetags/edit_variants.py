from django import template

register = template.Library()

@register.inclusion_tag('globals/edit_variants.html')
def edit_variants(id, url="", name="", value="", placeholder=""):
    return {
        'id': id, 
        'name': name if name else id,
        'url': url,
        'placeholder': placeholder,
        'value': value 
        }