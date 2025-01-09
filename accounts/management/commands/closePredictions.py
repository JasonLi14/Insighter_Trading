from django.core.management.base import BaseCommand, CommandError
from accounts.models import allPredictions, CustomUser
from datetime import datetime, timedelta

# Other libraries
import yfinance
import math

# The command that can now be used
# We can use cron to schedule this in deployment
class Command(BaseCommand):
    help = "Updates the predictions objects and changes accuracy of the users"

    def add_arguments(self, parser):  # Optional arguments
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        # Find predictions which are expired and close them
        current_date = datetime.today()  # For testing purposes
        expired_predictions = allPredictions.objects.filter(end_date__lt=current_date, counted=False)
        for prediction in expired_predictions:
            # Update the counted 
            prediction.counted = True

            # Update accuracy
            # Find the users involved
            prediction_user = prediction.user
            # Find the stock price they guessed
            predicted_price = float(prediction.end_value)
            # Find the time difference. More difference = more accuracy
            prediction_date = prediction.predict_date
            prediction_end = prediction.end_date
            change = prediction_end - prediction_date
            days = change.days
            
            # Find the stock involved
            ticker = prediction.ticker_id

            # Get the last price of each stock
            last_price = yfinance.Ticker(ticker).get_fast_info()["open"]

            # Find the score
            denominator = abs(last_price - predicted_price) + 0.1
            numerator = 0.005 * math.sqrt(days) * predicted_price
            score = math.log(numerator / denominator)
            
            # Calculate the new accuracy
            current_accuracy = float(prediction_user.accuracy)
            amount_predictions = prediction_user.completed_predictions
            new_accuracy = amount_predictions / (amount_predictions + 1) * current_accuracy + score / (amount_predictions + 1) 
            
            # Update fields
            prediction_user.accuracy = new_accuracy
            prediction_user.completed_predictions = prediction_user.completed_predictions + 1
            prediction_user.save()
        
        # Change the counted field
        allPredictions.objects.bulk_update(expired_predictions, ['counted'])     

        # Debug
        # print(CustomUser.objects.values_list('accuracy'))

