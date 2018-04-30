from django.db import models
from django.utils import timezone
# Create your models here.

from globals.models import Profile 
#from transport.models import Parcel, Delivery

class Comment(models.Model):
    author = models.ForeignKey(Profile)
    text = models.CharField(max_length=500)
    
class Notification(models.Model):
    receiver = models.ForeignKey(Profile)
    topic = models.CharField(max_length=100)
    text = models.CharField(max_length=500)
    
    @classmethod
    def create(cls, receiver, topic, text):
        obj = cls()
        obj.receiver = receiver
        obj.topic = topic
        obj.text = text
        obj.save()
        receiver.notify(topic, text)
        
class Message(models.Model):
    author = models.ForeignKey(Profile, related_name='authored_messages')
    receiver = models.ForeignKey(Profile, related_name='received_messages')
    text = models.CharField(max_length=500)
    reply_to = models.ForeignKey('Message', blank=True, null=True, related_name='answers')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{0}@{1}:{2}'.format(self.author, self.receiver, self.text)
    
    def get_time(self):
        #TODO: humanize
        return self.date
        
    def from_now(self):
        return timezone.now() - self.date
        
class Question(models.Model):
    message =models.ForeignKey(Message)
    parcel = models.ForeignKey('transport.Parcel', blank=True, null=True)
    trip = models.ForeignKey('transport.Trip', blank=True, null=True)
    
class Review(models.Model):
    message =models.ForeignKey(Message)
    parcel = models.ForeignKey('transport.Parcel', blank=True, null=True)
    trip = models.ForeignKey('transport.Trip', blank=True, null=True)
    rating = models.IntegerField()
