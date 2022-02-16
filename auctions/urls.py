from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("delete_from_watchlist/<int:listing_id>", views.delete_from_watchlist, name="delete_from_watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close_auction, name="close_auction"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
]
