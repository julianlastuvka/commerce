from typing import Callable
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}, id: {self.id}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=32, blank=True, default='')
    starting_bid = models.IntegerField()
    current_price = models.IntegerField(default=starting_bid, blank=True)
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winning_bids", blank=True, null=True, default=None)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    is_open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):

    bidder = ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidders")
    bid_value = models.IntegerField()
        
    def __str__(self):
        return f"Bid made by {self.bidder} on {self.listing}"

class Comment(models.Model):

    commenter = ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment_message = models.CharField(max_length=350)
    #add date and time? 

class Watched_listing(models.Model):

    user = ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    item = ForeignKey(Listing, on_delete=models.CASCADE)

