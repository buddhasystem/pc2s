import uuid
from django.db import models
from django.core.validators import *

class GlobalTag(models.Model):
    STATUS_CHOICES = [
        ('PUB', 'Published'),
        ('NEW', 'New'),
        ('INV', 'Invalid'),
    ]
    name		= models.CharField(max_length=128, primary_key=True, null=False, default="")
    status		= models.CharField(max_length=4, choices=STATUS_CHOICES, default='NEW')

class Payload(models.Model):
    uuid	    = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
    url		    = models.CharField(max_length=256, default="")
    
#-------------------------------------------------------------------------------    
# time		= models.BigIntegerField()
# time		= models.DateTimeField()

