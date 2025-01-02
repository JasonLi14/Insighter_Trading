# Other libraries
from datetime import date, datetime

# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template import loader
from django.http import HttpResponse, HttpRequest
from django.http import HttpResponseRedirect  # For reloading
from django.contrib.auth.decorators import login_required  # for pages that need logging in
from .forms import CustomUserCreationForm
from .forms import predictionForm  # Our prediction form to create predictions

# From our algorithms
from .algorithms import stock_graph as graphing 
from .algorithms import utility

# From our models
from .models import allPredictions

# From our queries
from . import queries

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required(login_url='/accounts/login/')
def viewStocks(request: HttpRequest, ticker, prediction):  # To view and predict stocks    
    template = loader.get_template("view_stock.html")
    # Template context date
    graph, stock_info = graphing.createStockGraph(ticker, 1)
    new_info = utility.roundDict(stock_info, 2)

    # Find prediction dates
    prediction_dates = utility.predictionDates()

    # Default prediction date
    if prediction == "0":
        prediction = prediction_dates[0]


    # Context for the view
    context: dict = {'title': 'View Stock',
                     'ticker': ticker,
                     'bar_plot': graph,
                     'stock_info': new_info,
                     'pred_dates': prediction_dates,
                     'chosen_date': prediction,
                     'predictions_list': queries.userPredictions(request.user)}
    
    # Set the maximum of the range to be dynamic
    range_change = round(float(new_info["lastPrice"]) * 0.2 * 4) / 4
    form_attrs = {
        "step": min(0.25, round(range_change / 5, 2)), 
        "min": -1 * range_change, 
        "max": range_change
    }

    # Processing prediction form
    if request.method == "POST":  
        # Fill the form with information from the post request
        form = predictionForm(data=request.POST, attrs=form_attrs)  
        # check if form is valid
        if form.is_valid():
            # Extract the change value
            prediction_change = form.cleaned_data["change"]
            # Get the user
            prediction_user = request.user
            # Get the ticker
            prediction_ticker = ticker
            # Get the end date of the prediction
            prediction_end_date = datetime.strptime(prediction, "%Y-%m-%d").date()
            # Get the current date
            prediction_curr_date = date.today()
            # Make a new predictions object
            new_prediction = allPredictions(
                ticker=prediction_ticker,
                user=prediction_user,
                predict_date=prediction_curr_date,
                end_date=prediction_end_date,
                change=prediction_change
            )
            new_prediction.save()
            # reload
            return HttpResponseRedirect(request.path_info)
    else:
        form = predictionForm(attrs=form_attrs, auto_id=False)  
        context["form"] = form    

    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def home(request):  # Profile page
    template = loader.get_template("home.html")
    context = {"user": request.user}
    return HttpResponse(template.render(context, request))
