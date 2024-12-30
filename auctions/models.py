from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass  # You can add custom fields if needed, like a profile picture or additional information


class AuctionListing(models.Model):
   
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)  # Optional field for an image
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    category = models.CharField(max_length=64, blank=True, null=True)
    highest_bidder = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_auctions') 
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Watchlist(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist') 
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='watchlisted_by') 
    added_at = models.DateTimeField(auto_now_add=True)
class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} on {self.listing.title} by {self.user.username}"


class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.listing.title}"

    
