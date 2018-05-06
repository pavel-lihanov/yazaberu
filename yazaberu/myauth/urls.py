from django.conf.urls import url
from django.contrib import admin
import myauth.views

urlpatterns = [
    url(r'^login/(?P<provider>[a-z]+)$', myauth.views.login_sn , name='login_sn'),
    url(r'^done$', myauth.views.done , name='login_sn_done'),
    url(r'^login$', myauth.views.login , name='login'),
    url(r'^register$', myauth.views.register , name='register'),
    url(r'^confirm$', myauth.views.confirm , name='confirm'),
    url(r'^welcome$', myauth.views.welcome , name='welcome'),
    url(r'^logout$', myauth.views.logout , name='logout'),
    url(r'^change_password$', myauth.views.change_password, name='change_password'),
]
