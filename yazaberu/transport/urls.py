from django.conf.urls import url
from django.contrib import admin
import transport.views

urlpatterns = [
    url(r'^parcel_search$', transport.views.parcel_search , name='parcel_search'),
    url(r'^trip_search$', transport.views.trip_search , name='trip_search'),
    url(r'^parcel/(?P<id>[0-9]+)$', transport.views.parcel, name='parcel'),
    url(r'^add_parcel$', transport.views.add_parcel, name='add_parcel'),
    url(r'^add_trip$', transport.views.add_trip, name='add_trip'),
]