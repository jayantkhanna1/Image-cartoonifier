
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("cartoonify",views.cartoonify,name="cartoonify"),
]
