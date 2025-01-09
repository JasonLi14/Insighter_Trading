# accounts/views.py

# Other libraries
from datetime import date, datetime

# Django 
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.http import HttpResponseRedirect  # For reloading
from django.contrib.auth.decorators import login_required  # for pages that need logging in

# changing password
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

# For creating user
from .forms import *

# For error handling
from django.db import IntegrityError
from django.contrib import messages  # For giving warning messages

# For paginating
from django.core.paginator import Paginator

# For searching
from django.db.models import Q

# From our algorithms
from .algorithms import stock_graph as graphing 
from .algorithms import utility

# From our models
from .models import allPredictions
from .models import stocks

# From our queries
from . import queries

# Authentication views
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("login")
    template_name = "registration/password_change.html"


@login_required(login_url='/accounts/login/')
def viewStocks(request: HttpRequest, ticker, prediction):  # To view and predict stocks    
    template = loader.get_template("view_stock.html")

    # Unsuccessful context
    fail_context: dict = {'title': 'View Stock',
            'success': False,
            'ticker': ticker,
            'bar_plot': None,
            'distribution_plot': None,
            'stock_info': None,
            'pred_dates': None,
            'chosen_date': prediction,
            'insighter_score': 0,
            'form': None,
            'votes': 0,
            'predictions_list': queries.userPredictions(request.user)}
    
    # Get data and catch errors with yfinance
    try:
        graph, stock_info = graphing.createStockGraph(ticker, 1)
        if stock_info['lastPrice'] is None:
            print("YFinance may not have the stock", ticker)
            return HttpResponse(template.render(fail_context, request))
    except KeyError:
        print("YFinance could not get the info for", ticker)
        return HttpResponse(template.render(fail_context, request))

    # Make a new_info dictionary
    new_info = utility.roundDict(stock_info, 2)

    # Find prediction dates
    prediction_dates = utility.predictionDates()

    # Find prediction dates string
    possible_dates = []
    for date in prediction_dates:
        possible_dates.append(date.strftime("%Y-%m-%d"))

    # Default prediction date
    if prediction == "0":
        prediction = prediction_dates[0]
    elif prediction not in possible_dates:
        # user entered their own prediction date
        return HttpResponseRedirect("0")

    distr_graph = None
    votes = 0
    insighter_score = 0
    # Check if the user predicted yet, otherwise distr_graph stays as none
    if len(allPredictions.objects.filter(ticker=ticker, end_date=prediction, user=request.user).values()) > 0:
        # Make a distribution graph
        # Change prediction values to floats
        prediction_values = []
        query = allPredictions.objects.filter(ticker=ticker, end_date=prediction)
        query_end_val = query.values_list('end_value')
        votes = len(query_end_val)
        for value in query_end_val:
            prediction_values.append(float(value[0]))
        print(prediction_values)
        distr_graph = graphing.createDistrGraph(prediction_values)

        # Calculate insighter score
        accuracy_sum = 1
        prediction_change_sum = 0
        for prediction_obj in query:
            user_accuracy = prediction_obj.user.accuracy
            user_prediction = prediction_obj.end_value
            prediction_change_sum += (float(user_prediction) - stock_info['lastPrice']) * float(user_accuracy)
            # Absolute sum on bottom
            accuracy_sum += abs(float(user_accuracy))
        insighter_change = prediction_change_sum / accuracy_sum
        insighter_score = insighter_change + stock_info['lastPrice']
        insighter_score = "${:.2f}".format(insighter_score)
            


    # Set the maximum of the range to be dynamic
    range_change = round(float(new_info["lastPrice"]) * 0.2 * 4) / 4
    form_attrs = {
        "step": min(0.25, round(range_change / 5, 2)), 
        "min": -1 * range_change, 
        "max": range_change
    }

    # Context for the view
    context: dict = {'title': 'View Stock',
                     'success': True,
                     'ticker': ticker,
                     'bar_plot': graph,
                     'distribution_plot': distr_graph,
                     'stock_info': new_info,
                     'pred_dates': prediction_dates,
                     'chosen_date': prediction,
                     'insighter_score': insighter_score,
                     'votes': votes,
                     'predictions_list': queries.userPredictions(request.user)}

    # Processing prediction form
    if request.method == "POST":  
        # Fill the form with information from the post request
        form = predictionForm(data=request.POST, attrs=form_attrs)  
        # check if form is valid
        if form.is_valid():
            try:
                # Extract the change value
                prediction_value = form.cleaned_data["change"] + float(new_info["lastPrice"])
                # Get the user
                prediction_user = request.user
                # Get the ticker
                prediction_ticker = stocks.objects.filter(ticker=ticker)[0]
                # Get the end date of the prediction
                prediction_end_date = prediction
                # Get the current date
                prediction_curr_date = date.today()
                # Make a new predictions object
                new_prediction = allPredictions(
                    ticker=prediction_ticker,
                    user=prediction_user,
                    predict_date=prediction_curr_date,
                    end_date=prediction_end_date,
                    end_value=prediction_value
                )
                new_prediction.save()
            except IntegrityError:
                messages.warning(request, "You cannot make duplicate predictions. ")
            return HttpResponseRedirect(request.path_info)
    else:
        form = predictionForm(attrs=form_attrs, auto_id=False)  
        context["form"] = form    

    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def home(request):  # Profile page
    template = loader.get_template("home.html")
    context = {"user": request.user,
               'predictions_list': queries.userPredictions(request.user),
               'accuracy': "{:.2f}".format(request.user.accuracy), 
               'count': request.user.completed_predictions}
    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def stocksList(request, page_number:int, search:str="search="):
    template = loader.get_template("stocks_list.html")
    if request.method == "POST":   # user is searching
        search_form = searchForm(request.POST)
        if search_form.is_valid():  # Form is valid 
            # Get the search prompt
            new_prompt = "search=" + search_form.cleaned_data["prompt"]
            # Redirect with new search prompt
            return HttpResponseRedirect(f"/accounts/predict/1/{new_prompt}")
        else:
            return HttpResponseRedirect(request.path_info)
    else:
        search_query=search[7:]
        pages_object = Paginator(stocks.objects
                                 .filter(Q(ticker__icontains=search_query) | Q(name__icontains=search_query))
                                 .order_by('ticker').values(), 25)  
        # Get to the current page
        page_obj = pages_object.get_page(page_number)

        # Get the  context
        context = {'predictions_list': queries.userPredictions(request.user),
                   'page_object': page_obj,
                   'show_back': False,
                   'prompt': search,
                   'prompt_partial': search_query,  
                   'search_form': searchForm}

        return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def predictionsList(request):
    template = loader.get_template("all_predictions.html")
    context = {
        "predictions": allPredictions.objects.filter(user=request.user).values() 
    }
    return HttpResponse(template.render(context, request))
