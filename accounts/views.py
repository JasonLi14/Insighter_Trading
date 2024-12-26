# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect  # For reloading
from django.contrib.auth.decorators import login_required  # for pages that need logging in
from .forms import CustomUserCreationForm
from .forms import predictionForm  # Our prediction form to create predictions

# From our algorithms
from .algorithms import stock_graph as graphing 
from .algorithms import utility



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required(login_url='/accounts/login/')
def viewStocks(request, ticker):  # To view and predict stocks    
    template = loader.get_template("view_stock.html")
    # Template context date
    graph, stock_info = graphing.createStockGraph(ticker, 1)
    new_info = {}

    for info in stock_info:  # Round everything to two digits:
        new_info[info] = stock_info[info]
        if type(stock_info[info]) == float:
            new_info[info] = '{:.2f}'.format(round(stock_info[info], 2))

    # Find prediction dates
    prediction_dates = utility.predictionDates()

    # Context for the view
    context: dict = {'title':    'View Stock',
                     'ticker': ticker,
                     'bar_plot': graph,
                     'stock_info': new_info,
                     'pred_dates': prediction_dates}
    if request.method == "POST":  # Processing form
        form = predictionForm(request.POST)  # Fill the form with information from the post request
        # check if form is valid
        if form.is_valid():
            # reload
            return HttpResponseRedirect(request.path_info)
    else:
        form = predictionForm()    
        context["form"] = form    

    return HttpResponse(template.render(context, request))


@login_required(login_url='/accounts/login/')
def home(request):  # Profile page
    template = loader.get_template("home.html")
    context = {"user": request.user}
    return HttpResponse(template.render(context, request))
