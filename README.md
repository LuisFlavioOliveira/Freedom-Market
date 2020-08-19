# Freedom-Market

Freedom Market is an e-commerce web application developed using Django, JavaScript, HTML, CSS and SQL. It's an online auction website where users can bid and create listings for online auctions.

The web application is design as an eBay-like e-commerce auction site that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

It was a very interesting project and I wanted to develop something that allows the user to negotiate in an online environment in real-time.


## The methodology 

On this web application, I've implemented the CRUD model. 

The CRUD paradigm is common in constructing web applications because it provides a memorable framework for reminding developers of how to 
construct full, usable models

To start, Through the Django's Admin Panel, the Admin can:

Create a user, a listing, a bid or a comment. 
Read all the information on the web application, such as the comments from a specific user
Update any listing, bid, comments or user's information
and Delete any user, listing, bid or comments
In the client-side, the user can add items to a Watchlist, post comments and create a listing with the option to close it once he is satisfied with the bids he received for his listing.


## Specifications about the source code 

The program was created using Django as Framework and SQLite3 as Database for the back-end; and HTML, CSS and JavaScript for the front-end.

The mainly application file is `auctions`. I've created 4 models inside of `models.py`:

* One for all the aspects of User (it heritages AbstractUser);
* One for the listing, where we have fields for the title of the listing, its category, description, image and etc;
* One for the bids that the users are gonna do for the listings;
* And one for the comments.

Regarding the `Watchlist`, I didn't want to create a Model only for that, so I choose the approach of creating a field watchlist inside of my `AuctionsListing` Model (the one for creates a listing). The idea was to create it using a `ManyToManyField` relationship with the Model `User` because a listing object can have many users watching it, that was my logic.

Like that, I had a slithy improvement in performance because it avoided creating an unnecessary table. I did some tests and the query was about 0.8s faster using this method.  

There's also a file called `myforms.py` where I've created the ModelsForms that allows the users to create an auction, to bid and to comment in a listing.

In my `views.py` file, the longest function is listing because it not only displays the listing object and its details, but it's also responsible to manage the bid form, to check if there's a winner for the bid already and the comments form. I choose this approach to concentrate it on listing to avoid creating long and numerous functions while I could concentrate it inside of one function without repeating myself. 


## Tools 

* Python 3.8.3 - The Back-End

* [Django](https://www.djangoproject.com/) - The Web Framework used

* [SQLite](https://www.sqlite.org/index.html) - Database Engine

* [BootStrap](https://getbootstrap.com/) - Front-End component (Menu)


## Screenshots and video

![HomePage](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Index%20page.png)

![Register](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Sign%20Up.png)

![HomePage](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/HomePage.png)

![Search Result](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Search%20page.png)

![Write](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Write.png)

![Diary](https://github.com/LuisFlavioOliveira/Covid-19_Diary/blob/master/screenshots/Diary.png)

![Video](https://youtu.be/1yfRc8rzqzo)



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 


### Prerequisites and Installing

You will need Python 3.x. and the latest version of Django. Type commands in terminal to install:

* Run `python -m pip install Django` to install Django

* Run `python manage.py makemigrations auctions` to make migrations for the `auctions` app.

* Run `python manage.py migrate` to apply migrations to your database.

* Finally, run `python manage.py runserver` to start the app server

If you want to create an Admin User, you can type the following command:

`python manage.py createsuperuser`


## License / Copyright

* Completed as project 2 of Harvard's CS50 Web Programming with Python and JavaScript
* This project is licensed under the MIT License.







