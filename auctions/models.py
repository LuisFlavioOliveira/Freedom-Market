from django.contrib.auth.models import AbstractUser
from django.db import models



# Iterable category choices
product_categories = (
    ("Collectibles & Arts", "Collectibles & Arts"),
    ("Electronics", "Electronics"),
    ("Entertainment memorabilia", "Entertainment memorabilia"),
    ("Fashion", "Fashion"),
    ("Home & Garden", "Home & Garden"),
    ("Motors", "Motors"),
    ("Sporting goods", "Sporting goods"),
    ("Toys & Hobbies", "Toys & Hobbies"),
    ("Other categories", "Other categories"),
)


class User(AbstractUser):
    pass



class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=25, choices=product_categories)
    image_url = models.URLField(blank=True)
    description = models.CharField(max_length=5000)
    product_price = models.DecimalField(max_digits=19, decimal_places=2)
    auction_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='create', null=True)
    watchlist = models.ManyToManyField(User, blank=True)
    status = models.BooleanField(default=False)
    

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_bid")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_id")
    bid = models.DecimalField(max_digits=19, decimal_places=2)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_comments")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listing_comments")
    comments = models.CharField(max_length=200)
    commented_date = models. DateTimeField(auto_now_add=True)

