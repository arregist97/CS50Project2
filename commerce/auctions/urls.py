from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing", views.listing, name="listing"),
    path("listing/<str:listing_id>", views.listing_view, name="listing_id"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
