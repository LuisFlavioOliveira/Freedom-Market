from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("expired", views.expired, name="expired"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.create_list, name="create_list"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("winner/<int:listing_id>", views.close_listing, name="close_listing"),
    path("comments/<int:listing_id>", views.comments, name="comments"),
    path("watching/", views.watching, name="watching"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category_name>", views.get_categories, name="get_categories")
]
