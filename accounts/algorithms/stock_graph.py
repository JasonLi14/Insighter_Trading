import  plotly.express      as      px
from    plotly.offline      import  plot
import  plotly.graph_objs   as      go
import  pandas              as      pd

# My own libraries
from . import get_data 

def createStockGraph(ticker: str, period: int) -> str:
    stock_data, company_name = get_data.getHistory(ticker, period) 
    # Create the plot
    labels = {
        "value": "Close Price",
        "Date": "Date and Time"
    }
    
    bar_plot = px.line(stock_data, labels=labels, title=f"{ticker} <br><sup>{company_name}</sup>")

    bar_plot.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(254, 253, 250)',
    })
    bar_plot.update_traces(line_color='#065143')
    bar_plot.update_layout(showlegend=False)


    # Embed the plot in an HTML div tag
    bar_plot_div: str = plot(bar_plot, output_type="div", config = {'staticPlot': True})
    return bar_plot_div


if __name__ == "__main__":
    createStockGraph("AAPL", 3)
    