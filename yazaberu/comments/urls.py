from django.conf.urls import url
from django.contrib import admin
import transport.views

urlpatterns = [
    url(r'^parcel/(?P<id>[0-9]+)/ask_question$', comments.views.ask_question, name='ask_question'),
]