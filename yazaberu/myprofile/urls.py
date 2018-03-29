from django.conf.urls import url
from django.contrib import admin
import myprofile.views

urlpatterns = [
    url(r'^$', myprofile.views.myprofile, name='myprofile'),
]