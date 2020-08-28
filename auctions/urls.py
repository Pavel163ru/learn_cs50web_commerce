from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("categories", views.categories, name="categories"),
    path("category/<slug:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("profile", views.profile, name="profile")
]
