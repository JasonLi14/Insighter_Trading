# This is for creating queries with our database
from .models import allPredictions

# This is to get all the predictions for a user
def userPredictions(user:str):
    all_data = allPredictions.objects.filter(user=user).values()
    print(all_data)
