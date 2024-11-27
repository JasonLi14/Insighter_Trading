import  plotly.express      as      px
from    plotly.offline      import  plot
import  plotly.graph_objs   as      go

def createGraph() -> str: 
    # Bar plot X axis values
    x_values = ["Sample 1", "Sample 2", "Sample 3"]

    # Bar plot Y axis values
    y_values = [1, 3, 2]

    # Create the plot
    bar_plot = go.Figure([go.Bar(x=x_values,
                                 y=y_values,
                                 textposition="auto")]) 

    # Embed the plot in an HTML div tag
    bar_plot_div: str = plot(bar_plot, output_type="div")
    return bar_plot_div
