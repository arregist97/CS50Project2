from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing", views.listing, name="listing"),
    path("listing/<str:listing_id>", views.listing_view, name="listing_id"),
    path("listing/<str:listing_id>/comment", views.comment, name="comment"),
    path("listing/<str:listing_id>/watch", views.watch, name="watch"),
    path("listing/<str:listing_id>/close", views.close, name="close"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
