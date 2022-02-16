from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import Comment, User, Listing, Watched_listing

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title:")
    description = forms.CharField(label="Description:", widget=forms.Textarea)
    starting_bid = forms.IntegerField(label="Starting bid:", min_value=1)
    url = forms.CharField(label="Image URL:", required=False)
    category = forms.CharField(label="Category")


def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": Listing.objects.filter(is_open = True)
    })


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


def create(request):

    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():

            listing = Listing(
                title = form.cleaned_data["title"],
                seller = request.user,
                description=form.cleaned_data["description"],
                category = form.cleaned_data["category"],
                starting_bid=form.cleaned_data["starting_bid"], 
                current_price = form.cleaned_data["starting_bid"],
                image_url = form.cleaned_data["url"]
                )   

            listing.save()


    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })

def listing(request, listing_id):

    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    on_watchlist = False

    if user.id:
        watchlist = user.watchlist.all()
        for item in watchlist:
            if item.item == listing:
                on_watchlist = True
                break

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "on_watchlist": on_watchlist,
        "comments": listing.listing_comments.all().order_by('-id')
    })

def watchlist(request):     

    return render(request, "auctions/watchlist.html", {
        "watchlist": [listing.item for listing in request.user.watchlist.all()]
    })

def add_to_watchlist(request, listing_id):

    if request.user.id:
        item = Listing.objects.get(pk=listing_id)
        watched = Watched_listing(user = request.user, item = item)
        watched.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def delete_from_watchlist(request, listing_id):

    watchlist = request.user.watchlist.all()

    for item in watchlist:
        if item.item.id == listing_id:
            item.delete()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def bid(request, listing_id):

    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        bid = int(request.POST.get('bid'))

        if bid > listing.current_price:
            listing.current_price = bid
            listing.highest_bidder = request.user
            listing.save()

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def close_auction(request, listing_id):

    if request.method == 'POST':

        listing = Listing.objects.get(pk=listing_id)
        listing.is_open = False
        listing.save()

    return HttpResponseRedirect("/")

def add_comment(request, listing_id):

    MAX_LENGTH = 200

    if request.method == "POST":

        listing =  Listing.objects.get(pk=listing_id)
        comment_message = request.POST.get('add_comment')

        if len(comment_message) <= MAX_LENGTH:
            new_comment = Comment(listing = listing, commenter = request.user,comment_message=comment_message)
            new_comment.save(force_insert=True)
            
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def categories(request):

    query_categories = Listing.objects.filter(is_open=True).values_list('category').distinct()

    categories = [c[0] for c in query_categories]

    return render(request, "auctions/categories.html", {
        'categories': categories 
    })



def category(request, category):

    listings = Listing.objects.filter(category = f'{category}', is_open=True)

    return render(request, "auctions/category.html", {
        'filtered_listings': listings,
        'category': category
    })