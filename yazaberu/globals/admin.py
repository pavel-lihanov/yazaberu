from django.contrib import admin

# Register your models here.

from .models import Profile, Avatar, Facebook, Vkontakte, GooglePlus, Yandex

# Register your models here.
admin.site.register(Profile)
admin.site.register(Avatar)
admin.site.register(Facebook)
admin.site.register(Vkontakte)
admin.site.register(GooglePlus)
admin.site.register(Yandex)