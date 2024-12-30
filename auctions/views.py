from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import User, AuctionListing, Bid, Comment, Watchlist, Category

def index(request): 
    listings = AuctionListing.objects.filter(is_active=True) 
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



def listing_detail(request, id):
    listing = get_object_or_404(AuctionListing, pk=id)
    latest_bid = Bid.objects.filter(listing=listing).order_by('-created_at').first()
    in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    is_creator = listing.user == request.user
    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "latest_bid": latest_bid,
        "in_watchlist": in_watchlist,
        "is_creator": is_creator
        })

def bids(request):
    if request.user.is_authenticated:
        user_bids = Bid.objects.filter(user=request.user).order_by('-created_at')
        return render(request, "auctions/bids.html", {"bids": user_bids})
    else:
        return HttpResponseRedirect(reverse("login"))
    
def create_listing(request): 
    if request.method == "POST": 
        title = request.POST["title"] 
        description = request.POST["description"] 
        starting_bid = request.POST["starting_bid"] 
        image_url = request.POST.get("image_url", "") 
        category = request.POST.get("category", "") # Create and save the new listing 
        listing = AuctionListing( 
            title=title, 
            description=description, 
            starting_bid=starting_bid, 
            image_url=image_url, 
            user=request.user,
            category=category, 
            is_active=True ) 
        listing.save() 
        return redirect("index") 
    return render(request, "auctions/create_listing.html")


def place_bid(request): 
    if request.method == "POST": 
        listing_id = request.POST.get("listing_id") 
        bid_amount = float(request.POST.get("bid_amount"))  # Convert bid_amount to float for comparison
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        
        # Check if the new bid is higher than the current bid
        if bid_amount <= listing.starting_bid:
           return HttpResponse("Your bid should be higher than the current bid.")
        

        else:# Create and save the new bid
            new_bid = Bid(listing=listing, user=request.user, amount=bid_amount)
            listing.current_price = bid_amount
            new_bid.save()

        # Update the current price of the listing
        
            listing.save()

            return redirect("bids")  # Redirect to bids page after submitting the bid 

    else: 
        listing_id = request.GET.get("listing_id") 
        listing = get_object_or_404(AuctionListing, pk=listing_id)
        return render(request, "auctions/place_bid.html", {"listing": listing})

def close_auction(request, id): 
    listing = get_object_or_404(AuctionListing, pk=id) 
    if listing.user != request.user: 
        return redirect("listing_detail", id=id) 
    latest_bid = Bid.objects.filter(listing=listing).order_by('-created_at').first() 
    if latest_bid: 
        listing.highest_bidder = latest_bid.user 
        listing.is_active = False 
        listing.closed = True 
        listing.save() 
        return redirect("listing_detail", id=id)

def add_to_watchlist(request): 
    if request.method == "POST": 
        listing_id = request.POST.get("listing_id") 
        listing = get_object_or_404(AuctionListing, pk=listing_id) # Add the listing to the user's watchlist
        Watchlist.objects.get_or_create(user=request.user, listing=listing) 
        return redirect("watchlist") 
def watchlist(request): 
    user_watchlist = Watchlist.objects.filter(user=request.user) 
    return render(request, "auctions/watchlist.html", {"watchlist": user_watchlist})

def categories(request): # Fetch all distinct categories from the AuctionListing model 
    categories = AuctionListing.objects.values_list('category', flat=True).distinct().exclude(category="") 
    return render(request, "auctions/categories.html", {"categories": categories}) 

def filter(request): # Get the category from the GET request 
    category = request.GET.get('category', '').lower() # Filter listings by the selected category 
    listings = AuctionListing.objects.filter(category__iexact=category) 
    return render(request, 'auctions/category.html', { 'listings': listings, 'category': category })

