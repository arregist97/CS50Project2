from django.contrib.auth.models import AbstractUser
from django.db import models


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=65536)
    current_price = models.FloatField()
    photo = models.BinaryField()

    def __str__(self):
        return f"{self.title}(${self.current_price})"

class User(AbstractUser):
    auctions_completed = models.IntegerField()
    listings = models.ManyToManyField(Listing, blank=True,related_name="listings")
    
    def __str__(self):
        return f"{self.username}({self.auctions_completed})"