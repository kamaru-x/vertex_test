from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    Qatar_ID = models.CharField(max_length=15,null=True,blank=True)
    Mobile = models.CharField(max_length=15,null=True,blank=True)
    Address = models.CharField(max_length=225,null=True,blank=True)
    Country = models.CharField(max_length=50,null=True,blank=True)
    is_salesman = models.BooleanField(default=False)