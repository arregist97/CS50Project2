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
    photo = models.CharField(max_length=256, blank=True, null=True)
    is_closed = models.BooleanField(default=False)
    category = models. CharField(max_length=64, null=True)

    def __str__(self):
        current_price = self.starting_price
        bids = Bid.objects.filter(listing=self)
        for bid in bids:
            if (bid.price >= current_price):
                current_price = bid.price

        return f"{self.title}(${current_price}):{self.id}"

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

class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} watching {self.listing}"

