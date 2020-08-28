from django.contrib.auth import authenticate, login, logout

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist
from django.contrib.auth.decorators import login_required
from .forms import ListingForm
from django.db.models import Count
from . import util


def index(request):
    
    # if request.user.is_authenticated:
    #     user = User.objects.get(pk=request.user.id)
    #     watchlistcount = user.watchlist.count()
    listings = Listing.objects.filter(state="active")
    return render(request, "auctions/index.html", {
        'listings': listings,
        'watchlistcount': util.watchlist_total(request)
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

@login_required
def newlisting(request):

    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            listing = Listing(
                title= form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                startbid = form.cleaned_data['startbid'],
                image = form.cleaned_data['image'],
                category = form.cleaned_data['category'],
                listedby = user,
                state = 'active',
                price = form.cleaned_data['startbid']
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = ListingForm()

    return render(request, "auctions/newlisting.html", {
        'form': form,
        'watchlistcount': util.watchlist_total(request)
    })

def listings(request, listing_id):
    if request.method == "POST":
        newbid = request.POST.get('newbid', '')
        watchbutton = request.POST.get('watchlist', 'not')
        submitbutton = request.POST.get('bidbutton', 'not')
        postbutton = request.POST.get('postbutton', 'not')
        closebutton = request.POST.get('closelisting', 'not')
        if watchbutton != 'not':
            listing = Listing.objects.get(pk=listing_id)
            user = User.objects.get(pk=request.user.id)
            if user.watchlist.filter(listing=listing).count() > 0:
                user.watchlist.filter(listing=listing).delete()
                # return HttpResponse("out watchbutton")
            else:
                watchlist = Watchlist(
                    user = User.objects.get(pk=request.user.id),
                    listing = Listing.objects.get(pk=listing_id)
                )
                watchlist.save()
                # return HttpResponse("in watchbutton")
                        
        elif submitbutton != 'not':
            listing = Listing.objects.get(pk=listing_id)
            bid = Bid(
                user = User.objects.get(pk=request.user.id),
                bid = newbid,
                listing = listing
            )
            bid.save()
            listing.price = bid.bid
            listing.save()
        elif postbutton != 'not':
            listing = Listing.objects.get(pk=listing_id)
            user = User.objects.get(pk=request.user.id)
            text = request.POST.get('comment', '')
            comment = Comment(listing=listing, user=user, content=text)
            comment.save()
        elif closebutton != 'not':
            listing = Listing.objects.get(pk=listing_id)
            listing.state = "closed"
            listing.wonuser = listing.bids.order_by("-bid").first().user
            listing.save()
        return HttpResponseRedirect(reverse("listings", args=[listing_id]))
       
    listing = Listing.objects.get(pk=listing_id)
    bids = listing.bids.count()
    currentbid = listing.bids.order_by("-bid").first()
    user = User.objects.get(pk=request.user.id)
    comments = listing.comments.all()

    if currentbid is not None and currentbid.user.id == request.user.id:
        yoursbid = True
    else: 
        yoursbid = False

    if currentbid is not None:
        newprice = currentbid.bid + 1
    else:
        newprice = listing.price + 1

    if Watchlist.objects.filter(user=user, listing=listing).count() > 0:
        watching = True
    else:
        watching = False

    return render(request, "auctions/listing.html", {
        "listing" : listing, 
        "bids" : bids,
        "lastbid": currentbid,
        "yoursbid": yoursbid,
        "newprice": newprice,
        "watching": watching,
        'watchlistcount': util.watchlist_total(request),
        "comments": comments    
    })

def categories(request):
    categories = Listing.objects.values("category").annotate(count=Count('category'))
    
    return render(request, "auctions/categories.html", {
        "categories": categories,
        'watchlistcount': util.watchlist_total(request)
    })

def category(request, category):
    if category == 'none':
        category = ''
    listings = Listing.objects.filter(category=category)
    if category == '':
        category = 'No Category'
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings,
        'watchlistcount': util.watchlist_total(request)
    })

def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watchlist = user.watchlist.all()
    listings = []
    for watched in watchlist:
        listings.append(watched.listing)

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        'watchlistcount': util.watchlist_total(request)
    })

def profile(request):
    user = User.objects.get(pk=request.user.id)
    ownactivelistings = Listing.objects.filter(listedby=user).filter(state="active")
    ownclosedlistings = Listing.objects.filter(listedby=user).filter(state="closed")
    
    wonlistings = Listing.objects.filter(wonuser=user).filter(state="closed")

    return render(request, "auctions/profile.html", {
        'ownactivelistings': ownactivelistings,
        "ownclosedlistings": ownclosedlistings,
        'wonlistings': wonlistings,
        'watchlistcount': util.watchlist_total(request)
    })