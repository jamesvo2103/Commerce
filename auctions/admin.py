from django.contrib import admin
from .models import User, AuctionListing, Bid, Comment

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    """Contains User model admin page config"""
    list_display = ("id", "username", "email", "password")

class AuctionListingAdmin(admin.ModelAdmin):
    """Contains AuctionListing model admin page config"""
    list_display = ("id", "title", "category", "starting_bid", "is_active", "created_at", "user")
    list_filter = ("is_active", "category", "created_at")
    search_fields = ("title", "description", "user__username", "category")
    list_editable = ("category",)

class BidAdmin(admin.ModelAdmin):
    """Contains Bid model admin page config"""
    list_display = ("listing", "user", "amount", "created_at")

class CommentAdmin(admin.ModelAdmin):
    """Contains Comment model admin page config"""
    list_display = ("listing", "user", "content")

#class WatchlistAdmin(admin.ModelAdmin):
 #   """Contains Watchlist model admin page config"""
#    list_display = ("auction", "user")

admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
#admin.site.register(Watchlist, WatchlistAdmin)

