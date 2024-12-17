from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    accuracy = models.DecimalField(max_digits=25, decimal_places=10)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.username