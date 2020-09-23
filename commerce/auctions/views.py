from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing, User
from django.contrib.auth.decorators import login_required
from django import forms



def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.all()
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
    price = forms.CharField(label="Price")

@login_required
def listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            seller = User.objects.get(username=request.user.username)

            listing = Listing(title=title, description=description, current_price=price, seller=seller)
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

def listing_view(request, listing_id):
    items = Listing.objects.all()
    try:
        item = items.get(pk=listing_id)
    except:
        return HttpResponse("Error: item number (" + listing_id + ") not found.<br>" + "<a href=" + "/" + ">Home</a>")
    return render(request, "auctions/listing_view.html", {
#        "message": "Are you logged in?",
        "title": item.title,
        "description": item.description,
        "listing_id": item.id,
        "current_price": item.current_price 
    })
