from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    auctions_completed = models.PositiveIntegerField(default=0) #Starts at zero, increments w each successful sell/buy
    
    def __str__(self):
        return f"{self.username}({self.auctions_completed})"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=65536)
    starting_price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    photo = models.CharField(max_length=256)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}(${self.starting_price}):{self.id}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username}(${self.price}):{self.listing.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=65536)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username}:{self.text}"