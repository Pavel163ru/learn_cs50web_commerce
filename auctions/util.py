from .models import User, Listing, Bid, Comment, Watchlist

def watchlist_total(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        watchlistcount = user.watchlist.count()
    else:   
        watchlistcount = ''
    return watchlistcount