from django.contrib import admin
from .models import AuctionListing, User, Bid, Comments

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comments)