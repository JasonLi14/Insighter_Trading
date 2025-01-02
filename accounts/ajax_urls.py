# accounts/urls.py
from django.urls import path

from .algorithms import ajax_functions  # For graphing
from . import views  # For graphing


urlpatterns = [
    path("change_graph/", ajax_functions.newGraph, name="change_range"),
]