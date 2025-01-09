# accounts/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("password_change/", views.ChangePasswordView.as_view(), name="password_change"),
    path("view_stock/<str:ticker>/<str:prediction>", views.viewStocks, name="view_stock"),
    path("home", views.home, name="home"),
    path("predict/<int:page_number>/<str:search>", views.stocksList, name="predict"),
    path("view_predictions", views.predictionsList, name="view_predictions"),
]