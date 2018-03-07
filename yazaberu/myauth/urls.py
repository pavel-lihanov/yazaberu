from django.conf.urls import url
from django.contrib import admin
import myauth.views

urlpatterns = [
    url(r'^login$', myauth.views.login , name='login'),
    url(r'^register$', myauth.views.register , name='register'),
    url(r'^confirm$', myauth.views.confirm , name='confirm'),
    url(r'^welcome$', myauth.views.welcome , name='welcome'),
]
