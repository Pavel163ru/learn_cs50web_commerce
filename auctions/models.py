from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    startbid = models.IntegerField()
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    listedby = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    state = models.CharField(max_length=64, blank=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)
    price = models.IntegerField()
    wonuser = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    content = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watching")