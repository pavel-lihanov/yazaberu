from django.conf.urls import url
from django.contrib import admin
import myprofile.views

urlpatterns = [
    url(r'^deliveries$', myprofile.views.mydeliveries, name='mydeliveries'),
    url(r'^parcels$', myprofile.views.myparcels, name='myparcels'),
    url(r'^messages$', myprofile.views.mymessages, name='mymessages'),
    #lists (returned from POST)
    url(r'^delivery_list$', myprofile.views.my_delivery_list, name='delivery_list'),
    url(r'^parcel_list$', myprofile.views.my_parcel_list, name='parcel_list'),
    url(r'^$', myprofile.views.myprofile, name='myprofile'),
]