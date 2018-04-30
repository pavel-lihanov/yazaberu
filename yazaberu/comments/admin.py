from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.

from .models import Message, Question, Review

# Register your models here.
admin.site.register(Message)
admin.site.register(Question)
admin.site.register(Review)