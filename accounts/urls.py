# accounts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("view_stock/<str:ticker>/<str:prediction>", views.viewStocks, name="view_stock"),
    path("home", views.home, name="home"),
]