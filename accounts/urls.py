# accounts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("view_stock/<str:ticker>/<int:period>/<int:prediction_date>", views.viewStocks, name="view_stock"),
    path("home", views.home, name="home")
]