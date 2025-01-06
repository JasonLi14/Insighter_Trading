import  plotly.express      as      px
from    plotly.offline      import  plot
import  plotly.graph_objs   as      go
import  pandas              as      pd
import plotly.figure_factory as ff

from random import random  # For testing
import numpy as np
# My own libraries
"""
from . import get_data


def createStockGraph(ticker: str, period: int) -> str:
    stock_data, company_name, fast_info = get_data.getHistory(ticker, period) 
    # Create the plot
    labels = {
        "value": "Close Price",
        "Date": "Date and Time"
    }

    bar_plot = px.line(stock_data, labels=labels, title=f"{ticker} <br><sup>{company_name}</sup>")

    bar_plot.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': '#fff9f8',
    })
    bar_plot.update_traces(line_color='#065143')
    bar_plot.update_layout(showlegend=False)

    # Embed the plot in an HTML div tag
    bar_plot_div: str = plot(bar_plot, output_type="div", config = {'staticPlot': True, 'responsive': True})
    return bar_plot_div, fast_info
"""

def createDistrGraph(data):
    dataframe = pd.DataFrame({"predictions": data})

    # Create distplot with curve_type set to 'normal'
    dist_plot = px.histogram(dataframe, x="predictions")

    # Add title
    dist_plot.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 
                             'paper_bgcolor': '#fff9f8', 
                             "title_text": 'Distplot with Normal Distribution', },)
    dist_plot.show()


if __name__ == "__main__":
    # createStockGraph("AAPL", 3)
    data = [] 
    for i in range(100):
        data.append(random())
    createDistrGraph(data)

    