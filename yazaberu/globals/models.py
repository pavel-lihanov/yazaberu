from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32)
    avatar = models.OneToOneField('Avatar', null=True)
    rider_rating = models.IntegerField(default=0)
    sender_rating = models.IntegerField(default=0)
    
    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
        
    @property
    def name_public(self):
        return '{0} {1}.'.format(self.first_name, self.last_name[0])
class Avatar(models.Model):
    image=models.ImageField(blank=True, null=True)
    
class Notification(models.Model):
    content = models.CharField(max_length=500)
    url = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    viewed=models.BooleanField(default=True)