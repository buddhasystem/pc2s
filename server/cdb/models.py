from django.db import models

class Tag(models.Model):
    STATUS_CHOICES = [
        ('PUB', 'Published'),
        ('NEW', 'New'),
        ('INV', 'Invalid'),
    ]
    name		= models.CharField(max_length=128, primary_key=True)
    description		= models.TextField(blank=True, null=True)
    status		= models.CharField(max_length=4, choices=STATUS_CHOICES, default='NEW')
    time		= models.BigIntegerField()


