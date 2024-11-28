import  plotly.express      as      px
from    plotly.offline      import  plot
import  plotly.graph_objs   as      go
import  pandas              as      pd

# My own libraries
import get_data 

def createStockGraph(ticker: str, period: int) -> str:
    stock_data = get_data.getHistory(ticker, period) 
    # Create the plot
    labels = {
        "value": "Close Price",
        "Date": "Date and Time"
    }
    bar_plot = px.line(stock_data, labels=labels, title=ticker)
    bar_plot.update_traces(line_color='Green')
    bar_plot.update_layout(showlegend=False)
    bar_plot.show()

    # Embed the plot in an HTML div tag
    bar_plot_div: str = plot(bar_plot, output_type="div")
    return bar_plot_div


if __name__ == "__main__":
    createStockGraph("AAPL", 3)