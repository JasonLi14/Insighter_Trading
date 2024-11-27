# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.template import loader
from django.http import HttpResponse

from .forms import CustomUserCreationForm

# From our algorithms
import algorithms.stock_graph as graphing 

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def viewStocks(request):
    template = loader.get_template("view_stock.html")
    # Template context date
    graph = graphing.createGraph()
    context: dict = {'title':    'View Stock',
                    'bar_plot': graph}

    return HttpResponse(template.render(context, request))
