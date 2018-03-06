from django import template

register = template.Library()

@register.inclusion_tag('globals/rating.html')
def rating(value, takes_context=True):
    print('rating("{0}")'.format(value))
    return {'stars': [i<value for i in range(5)]}