from django import template

register = template.Library()

@register.inclusion_tag('globals/avatar.html')
def avatar(profile, takes_context=True):
    return {'image': profile.get_avatar(), 'url': profile.get_url()}