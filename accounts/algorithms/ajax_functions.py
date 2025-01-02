# This page is for creating functions that will be accessed by jquery
from django.http import HttpRequest  # For datatyping
from django.http import HttpResponse  # For datatyping

from . import stock_graph as graphing 

def newGraph(request: HttpRequest):
    ticker = request.GET.get('ticker', None)
    period = int(request.GET.get('period', None))

    graph, stock_info = graphing.createStockGraph(ticker, period)
    return HttpResponse(graph)

