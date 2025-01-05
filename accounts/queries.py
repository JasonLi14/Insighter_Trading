# This is for creating queries with our database
from .models import allPredictions

# This is to get all the predictions for a user
def userPredictions(user:str, max=10):
    all_data = allPredictions.objects.filter(user=user).order_by("-end_date").values()
    return all_data[:max]


def hasUserMadePrediction(user:str, ticker:str, date:str):
    pass
