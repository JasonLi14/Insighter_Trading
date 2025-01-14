from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "completed_predictions", "accuracy"]


# Register my models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(allPredictions)
admin.site.register(stocks)
