from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    accuracy = models.DecimalField(max_digits=25, decimal_places=10, default=0)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.username   


class allPredictions(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'ticker', 'end_date'], name='unique_prediction') 
        ]

    # From the user database
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Other attributes
    ticker = models.CharField(max_length=10)
    predict_date = models.DateField()
    end_date = models.DateField()
    change = models.DecimalField(max_digits=6, decimal_places=3)
