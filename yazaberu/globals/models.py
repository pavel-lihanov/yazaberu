from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32)
    avatar = models.OneToOneField('Avatar', null=True)
    rider_rating = models.IntegerField(default=0)
    sender_rating = models.IntegerField(default=0)
    join_date = models.DateTimeField(auto_now_add=True)
    #don't calculate every time, update counters on delivery completion
    sent_parcel_count = models.IntegerField(default=0)
    completed_delivery_count = models.IntegerField(default=0)
    
    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
        
    def notify(self, topic, text):
        #TODO: notify method can be phone, email or both
        print('{0} should be notified of {1} ({2})'.format(self.name_public, topic, text) )
        
    @property
    def name_public(self):
        return '{0} {1}.'.format(self.first_name, self.last_name[0])
        
    def get_avatar(self):
        if self.avatar.image:
            return self.avatar.image.url
        else:
            return "/static/files/no-avatar.png"
            
    def get_url(self):
        return '/user/{0}'.format(self.id)

class Avatar(models.Model):
    image=models.ImageField(blank=True, null=True)
    
class Notification(models.Model):
    content = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    viewed=models.BooleanField(default=True)