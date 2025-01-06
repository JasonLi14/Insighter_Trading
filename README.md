# Insighter_Trading
This is a web application that will allow people to predict a stock's performance. It will then keep track of people's performance and do some data analytics with it. 

## Requirements and Libraries
The libraries used in this project include:
- Django
- Pandas
- Plotly
- Scipy

All the requirements to run this program can be found in the requirements.txt file.

## How to Run
These are the steps to run the program.
1. Navigate to Insighter_Trading/django_project/settings.py and ensure that the allowed hosts include the host that you wish to use.
2. Navigate to Insighter_Trading and type
``` 
py manage.py runserver
```
3. Create a cron job to run the command below every day at midnight.
``` 
py manage.py closePredictions
```