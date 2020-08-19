from django.forms import ModelForm, Textarea, TextInput, Select, URLInput, NumberInput
from . import models

# Iterable category choices
categories = (
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


class CreateAuction(ModelForm):
    class Meta:
        model = models.AuctionListing
        fields = ("title", "category", "image_url", "description", "product_price")
        widgets = {
            "title": TextInput(attrs={"class": "form-control"}),
            "category": Select(attrs={"class": "form-control"}),
            "image_url": URLInput(attrs={"class": "form-control"}),
            "description": Textarea(attrs={"size": "40", "class": "form-control"}),
            "product_price": NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Title",
            "categories": "Category",
            "image_url": "Product Image URL",
            "description": "Description",
            "product_price": "Starting Bid",
        }
        


class BidForm(ModelForm):
    class Meta:
        model = models.Bid
        fields = {"bid"}
        widgets = {"bid": NumberInput(attrs={"class": "bid-field form-control"})}
        labels = {"bid": ""}

class CommentsForm(ModelForm):
    class Meta:
        model = models.Comments
        fields = {"comments"}
        widgets = {
            "comments": Textarea(attrs={"size": "3000", "class": "comments-field form-control"})
        }
        labels = {"comments": ""}

        