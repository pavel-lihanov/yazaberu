from django import template
from comments.models import Message, Review
register = template.Library()

@register.inclusion_tag('myprofile/profile_menu.html')
def profile_menu(profile, active=0, takes_context=True):
    new_messages = Message.objects.filter(receiver=profile, review=None, viewed=False)
    new_reviews = Review.objects.filter(message__receiver=profile, message__viewed=False)
    items = [
      {'url':'/profile/', 'name':'Профиль','active': False,'count': 0},
      {'url':'/profile/messages', 'name':'Сообщения','active': False,'count': new_messages.count},
      {'url':'/profile/deliveries', 'name':'Ваши поездки','active': False,'count': 0},
      {'url':'/profile/parcels', 'name':'Отправления','active': False,'count': 0},
      {'url':'/profile/reviews', 'name':'Отзывы','active': False,'count': new_reviews.count},
    ]
    items[active]['active']=True
    return {'items':items}