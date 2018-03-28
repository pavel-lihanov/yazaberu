from django.contrib import admin

# Register your models here.

from .models import Profile, Avatar

# Register your models here.
admin.site.register(Profile)
admin.site.register(Avatar)