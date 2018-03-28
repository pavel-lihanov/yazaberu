from django.db import models

# Create your models here.

from globals.models import Profile 
from transport.models import Parcel, Delivery

class Comment(models.Model):
    author = models.ForeignKey(Profile)
    text = models.CharField(max_length=500)