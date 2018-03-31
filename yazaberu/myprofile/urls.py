from django.conf.urls import url
from django.contrib import admin
import myprofile.views

urlpatterns = [
    url(r'^deliveries$', myprofile.views.mydeliveries, name='mydeliveries'),
    url(r'^parcels$', myprofile.views.myparcels, name='myparcels'),
    url(r'^messages$', myprofile.views.mymessages, name='mymessages'),
    url(r'^$', myprofile.views.myprofile, name='myprofile'),
]