from django.conf.urls import url
from django.contrib import admin
import transport.views

urlpatterns = [
    url(r'^parcel_search$', transport.views.parcel_search , name='parcel_search'),
    url(r'^trip_search$', transport.views.trip_search , name='trip_search'),
    url(r'^parcel/(?P<id>[0-9]+)$', transport.views.parcel, name='parcel'),
    url(r'^add_parcel$', transport.views.add_parcel, name='add_parcel'),
    url(r'^add_trip$', transport.views.add_trip, name='add_trip'),
    url(r'^trip/(?P<id>[0-9]+)/deal$', transport.views.trip_deal, name='trip_deal'), #note: no page yet
    url(r'^parcel/(?P<id>[0-9]+)/deal$', transport.views.parcel_deal, name='parcel_deal'),
    url(r'^offer/(?P<id>[0-9]+)/accept$', transport.views.accept_offer, name='accept_offer'),
    url(r'^offer/(?P<id>[0-9]+)/decline$', transport.views.decline_offer, name='decline_offer'),
    url(r'^parcel/(?P<id>[0-9]+)/offer_trip$', transport.views.offer_trip, name='offer_trip'),
    url(r'^trip/(?P<id>[0-9]+)/offer_parcel$', transport.views.offer_parcel, name='offer_parcel'),
]