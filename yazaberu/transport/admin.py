from django.contrib import admin

# Register your models here.

from .models import City, Location, Parcel, Route, Trip, Delivery

# Register your models here.
admin.site.register(City)
admin.site.register(Location)
admin.site.register(Parcel)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(Delivery)