from django.db import models
from django.db.models import Min, Max, Sum, Count

# Create your models here.

from globals.models import Profile

class City(models.Model):
    name=models.CharField(max_length=100)
    #region=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    
    def __str__(self):
        return '{0}, {1}'.format(self.name, self.country)
    
class Location(models.Model):
    city=models.ForeignKey(City)
    lat=models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    lng=models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    address=models.CharField(max_length=255)

    def __str__(self):
        return '{0} @ {1}'.format(self.address, self.city)

class Parcel(models.Model):
    #short description of what's in the parcel
    description=models.CharField(max_length=255)
    #owner
    owner=models.ForeignKey(Profile)
    #approx weight in kg
    weight=models.IntegerField(default=1)
    #declared value in RUB
    value=models.IntegerField(default=0)
    #max delivery price
    max_price=models.IntegerField(default=0)
    #photo
    image=models.ImageField(null=True)
    #location from where the parcel is sent, address is used as meeting place
    origin=models.ForeignKey(Location, related_name='parcels_from', null=True)
    #location to where the parcel should be delivered
    destination=models.ForeignKey(Location, related_name='parcels_to', null=True)
    #when the parcel was created
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    #date by which the parcel should be delivered
    due_date = models.DateTimeField(null=True)
    #additional comment by owner
    comment=models.CharField(max_length=500, default='')

    def __str__(self):
        return self.description
        
class Route(models.Model):
    start=models.ForeignKey(City, related_name='starts')
    end=models.ForeignKey(City, related_name='ends')
    
    def __str__(self):
        return 'Route from {0} to {1}'.format(self.start, self.end)
        
    def min_price(self):
        return 55
        
    def avg_time(self):
        return 2
    
class Trip(models.Model):
    rider=models.ForeignKey(Profile)
    route=models.ForeignKey(Route)
    transport=models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    #auto-updated when start and end date
    duration = models.IntegerField()
    price = models.IntegerField(default=0)
    max_weight = models.IntegerField(default=5)
    def __str__(self):
        return 'Trip {0} by {1} @ {2}'.format(self.route, self.rider, self.start_date)

class Delivery(models.Model):
    #what is delivered
    parcel=models.ForeignKey(Parcel)
    #the route where the parcel will go
    trip=models.ForeignKey(Trip, blank=True, null=True)
    #agreed price
    price = models.IntegerField()
    #when rider got the parcel
    start_date = models.DateTimeField(blank=True, null=True)
    #when rider delivered the parcel
    end_date = models.DateTimeField(blank=True, null=True)
    #auto-updated when start and end date are set
    duration = models.IntegerField()
    delivered=models.BooleanField()
    rating = models.DecimalField(default=5.0, max_digits=2, decimal_places=1)
    
    def __str__(self):
        return 'Delivery of {0} to {1} @ {2}'.format(self.parcel, self.trip.route.end, self.start_date)
        
    def complete(self, rating=None, comment=None):
        self.trip.rider.completed_delivery.count += 1
        self.parcel.owner.sent_parcel_count += 1
        if rating is not None:
            self.self.trip.rider.update_rating(rating)
        if comment is not None:
            self.self.trip.rider.comment_set.add(comment)
        self.trip.rider.save()
        self.parcel.owner.save()

class Offer(models.Model):
    parcel = models.ForeignKey(Parcel)
    trip = models.ForeignKey(Trip)
    price = models.IntegerField(default=0)

#TODO: most popular routes
def get_popular_routes(cnt=3):
    return list(Route.objects.all())[-cnt:]
    
#TODO: filter only "pretty" deliveries
def get_advert_delivered(cnt=3):
    return list(Delivery.objects.all())[-cnt:]
    
def min_price(start_city, end_city):
    routes=Delivery.objects.filter(trip__route__start__city=start_city, trip__route__end__city=end_city)
    return routes.aggregate(Min(price))

#TODO: filter 
def avg_time(start_city, end_city):
    routes=Delivery.objects.filter(trip__route__start__city=start_city, trip__route__end__city=end_city, delivered=True)
    return routes.aggregate(Min(price))
    
def waiting_parcels_count():
    return Parcel.objects.filter(delivery=None).count()

def riders_count():
    #return Trip.objects.distinct('rider').count()
    #TODO: implement (sqlite does not support distinct)
    return 5

def delivered_parcels_count():
    return Delivery.objects.filter(delivered=True).count()
    
def total_income():
    return Delivery.objects.filter(delivered=True).aggregate(Sum('price'))['price__sum']
