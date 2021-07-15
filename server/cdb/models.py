from django.db import models

class Tag(models.Model):
    STATUS_CHOICES = [
        ('PUB', 'Published'),
        ('NEW', 'New'),
        ('INV', 'Invalid'),
    ]
    id	        = models.AutoField(primary_key=True,  verbose_name="ID")
    name		= models.CharField(max_length=128)
    description	= models.TextField(blank=True, null=True)
    status		= models.CharField(max_length=4, choices=STATUS_CHOICES, default='NEW')
    time		= models.DateTimeField()

class Payload(models.Model):
    id	        = models.AutoField(primary_key=True,  verbose_name="ID")   
    name		= models.CharField(max_length=128)
    description	= models.TextField(blank=True, null=True)
    time		= models.BigIntegerField()


