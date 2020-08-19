from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django import forms

from .models import User, AuctionListing, Bid, Comments, product_categories
from . import myforms


def index(request):
    # Render the index page if user authenticated
    if request.user.is_authenticated:
        return render(
            request,
            "auctions/index.html",
            {"auctions": AuctionListing.objects.filter(status=False)},
        )
    # render the mainpage user not authenticated
    else:
        return render(request, "auctions/mainpage.html")


# Function to display the expired listings
def expired(request):
    return render(
        request,
        "auctions/expired.html",
        {"auctions": AuctionListing.objects.filter(status=True)},
    )

# Login function
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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_list(request):
    """ Function to create a new list using a model form  """
    if request.method == "POST":
        form = myforms.CreateAuction(request.POST)

        if form.is_valid():
            form.save()
            # call "created" function
            created(request, AuctionListing)
            return HttpResponseRedirect(reverse("index"))
        else:
            # We pass form as context for the use see the error
            # if the form doesn't pass the is_valid check
            return render(request, "auctions/create_listing.html", {"form": form})

    # If request method is 'GET', return just an empty form
    return render(
        request, "auctions/create_listing.html", {"form": myforms.CreateAuction()}
    )


@login_required
def listings(request, listing_id):

    """ The listings function is responsible for many user interactions on
    the web application. 
    
    It's mainly function is to display the listing the user selected and its details. 
    
    It's also responsible for implementing the Bid model that will allow the user
    to bid and to define which user won the auction.
    """

    # Get the listing object that the user is currently viewing
    listing_check = AuctionListing.objects.get(pk=listing_id)
    # Order the comments by desc. date
    get_comments = Comments.objects.filter(listing=listing_id).order_by(
        "-commented_date"
    )

    # Get the comments form
    comments_form = myforms.CommentsForm(request.POST)

    # Get the last bid
    # If there's already a current highest bid inside, try it
    try:
        check_bid = Bid.objects.filter(listing=listing_id).order_by("-bid")[0]
        current_bid = check_bid.bid
    # if there isn't a current highest bid, create one with value 0
    except:
        current_bid = 0

    ### Implementation of the Bid action ###
    if request.method == "POST":

        form = myforms.BidForm(request.POST)

        # Check if the user's bid is higher than the starting bid
        if float(request.POST["bid"]) <= float(listing_check.product_price):
            messages.error(
                request,
                f"Your bid must be higher than the starting bid of ${listing_check.product_price}",
                extra_tags="warning",
            )

        else:
            # Check if the user's bid is higher than the last current bid
            if float(request.POST["bid"]) > float(current_bid):
                if form.is_valid():
                    # the snipper below insert the user.id and listing.id to the bid table
                    obj = form.save(commit=False)
                    obj.user = User.objects.get(pk=request.user.id)
                    obj.listing = AuctionListing.objects.get(pk=listing_id)
                    obj.save()
                    messages.success(
                        request, f"You just bid ${request.POST['bid']}! Good luck!"
                    )
                    return HttpResponseRedirect(reverse("listings", args=[listing_id]))

                # if form is not valid, render the form and show the errors
                else:
                    return render(request, "auctions/listings.html", {"form": form})

            # if user's bid isn't higher than the last bid
            else:
                messages.error(
                    request,
                    f"Your bid must be higher than the last bid of ${current_bid}",
                    extra_tags="warning",
                )

    # Get if the user's bid is the current bid
    is_current_bid = False
    try:
        get_user_bid = Bid.objects.filter(listing=listing_id).order_by("-bid")[0]
        # check if the lastest highest bid was made by the current user
        if (
            get_user_bid.user.id == request.user.id
            and get_user_bid.listing.id == listing_id
        ):
            is_current_bid = True

        else:
            is_current_bid
    except:
        is_current_bid = False




    # Get the current number of bits on the listing
    bids_quantity = len(Bid.objects.filter(listing=listing_id))

    ### END of the Bid action code ###


    ### Implement the winner code to get the winner of the current auction ###
    # If request.method == "GET"

    # Booleans
    winner = False
    user_creator = False
    no_winner = False

    # check if the user in the listing is the user that created it
    if request.user == listing_check.created_by:
        user_creator = True
    else:
        user_creator

    # Determine if the listing is close and if close, get the winner
    if listing_check.status is True:
        # try to get the highest bid
        try:
            get_winner = Bid.objects.filter(listing=listing_id).order_by("-bid")[0]
            # check if the current user is the winner
            if get_winner.user == request.user:
                winner = True
        except:
            winner = False
            no_winner = True

    # Finally, render all the relevant information
    return render(
        request,
        "auctions/listings.html",
        {
            "listing": AuctionListing.objects.get(pk=listing_id),
            "form": myforms.BidForm(),
            "comments_form": myforms.CommentsForm(),
            "bids_quantity": bids_quantity,
            "is_current_bid": is_current_bid,
            "current_bid": current_bid,
            "user_creator": user_creator,
            "winner": winner,
            "get_comments": get_comments,
            "no_winner": no_winner,
        },
    )


# Function to get the user who created a listing
# https://stackoverflow.com/questions/52871997/get-current-user-for-created-by-field-in-model-class
@login_required
def created(request, model):
    obj = model.objects.latest("pk")
    if obj.created_by is None:
        obj.created_by = request.user
    obj.save()

# function to add listings to user's watchlist
@login_required
def watchlist(request, listing_id):
    """ Function that implements the watchlist button  """

    # Get the information about the current listing
    check = AuctionListing.objects.get(pk=listing_id)

    # if user is watching it already, remove it
    if check.watchlist.filter(pk=request.user.id):
        check.watchlist.remove(request.user)
        check.save()
        messages.error(
            request, "You remove this item from your watchlist", extra_tags="warning"
        )

    # if NOT watching, add it
    else:
        check.watchlist.add(request.user)
        check.save()
        messages.success(request, "You successfully added it to your watchlist")

    return HttpResponseRedirect(reverse("listings", args=[listing_id]))

# Function to display the watchlist of the user
@login_required
def watching(request):
    return render(
        request,
        "auctions/watching.html",
        {"watchings": AuctionListing.objects.filter(watchlist=request.user.id)},
    )

# function that allows the user to close the listing he created
@login_required
def close_listing(request, listing_id):
    """ Function that allows the user who created the listing to close it """

    if request.method == "POST":
        check_close = AuctionListing.objects.get(pk=listing_id)
        check_close.status = True
        check_close.save()
        return HttpResponseRedirect(reverse("index"))

# function to display the categories
@login_required
def categories(request):
    return render(
        request, "auctions/categories.html", {"categories": product_categories}
    )

# Function that display all listings inside that category
@login_required
def get_categories(request, category_name):
    return render(
        request,
        "auctions/category.html",
        {"auctions": AuctionListing.objects.filter(category=category_name)},
    )

# Function to post and see comments in the listings
@login_required
def comments(request, listing_id):
    comments_form = myforms.CommentsForm(request.POST)
    if request.method == "POST":
        if comments_form.is_valid():
            obj_comments = comments_form.save(commit=False)
            obj_comments.user = User.objects.get(pk=request.user.id)
            obj_comments.listing = AuctionListing.objects.get(pk=listing_id)
            obj_comments.save()
            return HttpResponseRedirect(reverse("listings", args=[listing_id]))
        else:
            return HttpResponseRedirect(reverse("listings", args=[listing_id]))
