from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    auctions_completed = models.PositiveIntegerField(default=0) #Starts at zero, increments w each successful sell/buy
    
    def __str__(self):
        return f"{self.username}({self.auctions_completed})"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=65536)
    current_price = models.FloatField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    photo = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.title}(${self.current_price}):{self.id}"

