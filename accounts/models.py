from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    accuracy = models.DecimalField(max_digits=25, decimal_places=10, default=0)
    completed_predictions = models.IntegerField(default=0)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.username   


class stocks(models.Model):
    ticker = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=1000)
    exchange = models.CharField(max_length=1000)


class allPredictions(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'ticker', 'end_date'], name='unique_prediction') 
        ]
    # From the user database
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Other attributes
    ticker = models.ForeignKey(stocks, on_delete=models.CASCADE)
    predict_date = models.DateField()
    end_date = models.DateField()
    end_value = models.DecimalField(max_digits=6, decimal_places=3)
    counted = models.BooleanField(default=False)

