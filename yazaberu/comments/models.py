from django.db import models

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
    reply_to = models.ForeignKey('Message', blank=True, null=True)