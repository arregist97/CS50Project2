from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing, User, Bid, Comment, Watch
from django.contrib.auth.decorators import login_required
from django import forms



def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.filter(is_closed=False)
    })

def categories(request):
    return render(request, "auctions/categories.html")

def category(request, category_id):
    
    return render(request, "auctions/category.html", {
        "Title": category_id.capitalize(),
        "Listings": Listing.objects.filter(is_closed=False),
        "Category": category_id
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

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={"style": "resize: none;"}), label="Description")
    price = forms.FloatField(label="Price")
    image = forms. CharField(label="Image URL", required=False)
    category= forms.CharField(label='Category', widget=forms.Select(choices=[('other', 'Other'),
    ('sports', 'Sports'),
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ]))

@login_required(login_url='/login')
def listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            seller = User.objects.get(username=request.user.username)
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]

            listing = Listing(title=title, description=description, starting_price=price, seller=seller, photo=image, category=category)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/listing.html", {
                "form": form
            })
    else:
        return render(request, "auctions/listing.html", {
            "form": NewListingForm()
        })

class NewBidForm(forms.Form):
    price = forms.FloatField(label="Price")

class NewCommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"style": "resize: none;"}), label="Comment")

def listing_view(request, listing_id):
    items = Listing.objects.all()
    try:
        item = items.get(pk=listing_id)
    except:
        return HttpResponse("Error: item number (" + listing_id + ") not found.<br>" + "<a href=" + "/" + ">Home</a>")
    
    

    #Obtain the user 
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)        

    current_price = item.starting_price
    bids = Bid.objects.filter(listing=Listing.objects.get(id=listing_id))
    winner = None
    for bid in bids:
        if (bid.price >= current_price):
            current_price = bid.price
            if item.is_closed:
                winner = bid.user                
    
    comments = Comment.objects.filter(listing=Listing.objects.get(id=listing_id))
    #Determine watching (ie whether user is already watching this item)
    watching = (request.user.is_authenticated) and (len(Watch.objects.filter(user=request.user).filter(listing=item)) >=1) 

    if request.method == "POST" and not item.is_closed:
        if request.user.is_authenticated:
            bidform = NewBidForm(request.POST)
            if bidform.is_valid():
                price = bidform.cleaned_data["price"]
                listing = Listing.objects.get(id=listing_id)

                if(price <= current_price):
                    return render(request, "auctions/listing_view.html", {
                    "message": "Price must be higher than current price: " + str(current_price) + ".",
                    "listing": item,
                    "User": request.user,
                    "current_price": current_price,
                    "bids": bids,
                    "bidform": bidform,
                    "commentform": NewCommentForm,
                    "comments": comments,
                    "is_watching": watching,
                    "winner": winner
                })

                bid = Bid(user=user, price=price, listing=listing)
                bid.save()
                return HttpResponseRedirect(reverse("listing_id", args=(listing_id,)))
            else:
            
                return render(request, "auctions/listing_view.html", {
                    "listing": item,
                    "User": request.user,
                    "current_price": current_price,
                    "bids": bids,
                    "bidform": bidform,
                    "commentform": NewCommentForm,
                    "comments": comments,
                    "is_watching": watching,
                    "winner": winner
                })
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
                    
        return render(request, "auctions/listing_view.html", {
            "listing": item,
            "User": request.user,
            "current_price": current_price,
            "bids": bids,
            "bidform": NewBidForm,
            "commentform": NewCommentForm,
            "comments": comments,
            "is_watching": watching,
            "winner": winner
        })

@login_required(login_url='/login')  
def comment(request, listing_id):
    print(listing_id)
    items = Listing.objects.all()
    try:
        item = items.get(pk=listing_id)
    except:
        return HttpResponse("Error: item number (" + listing_id + ") not found.<br>" + "<a href=" + "/" + ">Home</a>")

    current_price = item.starting_price
    bids = Bid.objects.filter(listing=Listing.objects.get(id=listing_id))
    winner = None
    for bid in bids:
        if (bid.price >= current_price):
            current_price = bid.price
            if item.is_closed:
                winner = bid.user 
    
    comments = Comment.objects.filter(listing=Listing.objects.get(id=listing_id))
    #Determine watching (ie whether user is already watching this item)
    watching = (request.user.is_authenticated) and (len(Watch.objects.filter(user=request.user).filter(listing=item)) >=1)

    if request.method == "POST":
        commentform = NewCommentForm(request.POST)
        if commentform.is_valid():
            user = User.objects.get(username=request.user.username)
            text = commentform.cleaned_data["comment"]
            listing = Listing.objects.get(id=listing_id)

            comment = Comment(user=user, text=text, listing=listing)
            comment.save()
            print(listing_id)
            return HttpResponseRedirect(reverse("listing_id", args=(listing_id,)))
        else: 
            return render(request, "auctions/listing_view.html", {
                "listing": item,
                "User": request.user,
                "current_price": current_price,
                "bids": bids,
                "bidform": NewBidForm,
                "commentform": commentform,
                "comments": comments,
                "is_watching": watching,
                "winner": winner
            })
    else:
    
        return HttpResponseRedirect(reverse("listing_id", args=(listing_id,)))

@login_required(login_url='/login')
def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if listing.seller.username == request.user.username:
        listing.is_closed = True
        listing.save()      
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url='/login')
def watch(request, listing_id):
    if request.method == "POST":
        #Check listing id is valid
        items = Listing.objects.all()
        try:
            item = items.get(pk=listing_id)
        except:
            return HttpResponse("Error: item number (" + listing_id + ") not found.<br>" + "<a href=" + "/" + ">Home</a>")
        #Check whether user is already watching this item
        user = User.objects.get(username=request.user.username)
        items_watched = Watch.objects.filter(user=user).filter(listing=item)
        print(len(items_watched))
        if len(items_watched) >=1:             
            items_watched.delete() #Remove the watch(s)
            #return HttpResponse("You are no longer watching item (" + listing_id + ") .<br>" + "<a href=" + reverse("listing_id", args=listing_id) + ">Back to listing</a>")
        else:
            #Create and save the new watch
            watch = Watch(user=user,listing=item)
            watch.save()
            #return HttpResponse("You are now watching item (" + listing_id + ") .<br>" + "<a href=" + reverse("listing_id", args=listing_id) + ">Back to listing</a>")
        return HttpResponseRedirect(reverse("listing_id", args=(listing_id,)))

@login_required(login_url='/login')
def watching(request):
    user = User.objects.get(username=request.user.username)
    return render(request, "auctions/watching.html", {
        "Watches": Watch.objects.filter(user=user),
    })

