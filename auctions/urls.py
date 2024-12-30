from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bids", views.bids, name="bids"),
    path("listing/<int:id>/", views.listing_detail, name="listing_detail"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("place_bid", views.place_bid, name="place_bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"),
    path("categories", views.categories, name="categories"),
    path("filter", views.filter, name="filter"),
   path("close_auction/<int:id>/", views.close_auction, name="close_auction"),
]
