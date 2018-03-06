from django.db import models

# Create your models here.

from globals.models import Profile

class City(models.Model):
    name=models.CharField(max_length=100)
    #region=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    
    def __str__(self):
        return '{0}, {1}'.format(self.name, self.country)
    
class Parcel(models.Model):
    description=models.CharField(max_length=255)
    owner=models.ForeignKey(Profile)
    image=models.ImageField()
    def __str__(self):
        return self.description
        
class Location(models.Model):
    city=models.ForeignKey(City)
    lat=models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    lng=models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    address=models.CharField(max_length=255)

    def __str__(self):
        return '{0} @ {1}'.format(self.address, self.city)
        
class Route(models.Model):
    start=models.ForeignKey(City, related_name='starts')
    end=models.ForeignKey(City, related_name='ends')
    
    def __str__(self):
        return 'Route from {0} to {1}'.format(self.start, self.end)
    
class Trip(models.Model):
    rider=models.ForeignKey(Profile)
    route=models.ForeignKey(Route)
    transport=models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    #auto-updated when start and end date
    duration = models.IntegerField()
    
    def __str__(self):
        return 'Trip {0} by {1} @ {2}'.format(self.route, self.rider, self.start_date)

class Delivery(models.Model):
    parcel=models.ForeignKey(Parcel)
    trip=models.ForeignKey(Trip, blank=True, null=True)
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