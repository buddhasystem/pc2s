import uuid
from datetime import datetime

from django.utils import timezone

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
    timestamp   = models.DateTimeField(default=timezone.now)

class GlobalTagMap(models.Model):
    id          = models.AutoField(primary_key=True)
    globaltag	= models.CharField(max_length=128, null=False, default="")
    tag		    = models.CharField(max_length=128, null=False, default="")

class Tag(models.Model):
    name		= models.CharField(max_length=128, primary_key=True, null=False, default="")
    timestamp   = models.DateTimeField(default=timezone.now)

class IOV(models.Model):
    since       = models.DateTimeField(default=timezone.now)
    payload	    = models.UUIDField(null=True)

class Payload(models.Model):
    id          = models.AutoField(primary_key=True)
    url		    = models.CharField(max_length=256, default="")


