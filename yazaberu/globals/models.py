from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32)
    avatar = models.OneToOneField('Avatar', null=True)
    
    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
        
class Avatar(models.Model):
    image=models.ImageField(blank=True, null=True)