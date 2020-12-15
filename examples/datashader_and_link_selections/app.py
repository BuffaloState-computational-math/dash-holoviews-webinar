# Load iris dataset and replicate with noise to create large dataset
from plotly.data import iris
import numpy as np
import pandas as pd
df_original = iris()[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
df = pd.concat([
    df_original + np.random.randn(*df_original.shape) * 0.1
    for i in range(10000)
])

# Build HoloViews Dataset from large Pandas DataFrame
import holoviews as hv
from holoviews.plotting.plotly.dash import to_dash
dataset = hv.Dataset(df)

# Build Datashaded Scatter and Histogram HoloViews Elements, and side-by-side layout
from holoviews.operation.datashader import datashade
scatter = datashade(
    hv.Scatter(dataset, kdims=["sepal_length"], vdims=["sepal_width"])
)
hist = hv.operation.histogram(
    dataset, dimension="petal_width", normed=False
)
row = scatter + hist

# Link selections across subplots
linked_row = hv.selection.link_selections(row)

# Set plot title
linked_row.opts(title="Datashader with %d points" % len(dataset))

# Build Dash app
import dash
app = dash.Dash(__name__)
components = to_dash(
    app, [linked_row], reset_button=True
)

# Build Dash layout
import dash_html_components as html
app.layout = html.Div(components.children)

if __name__ == "__main__":
    app.run_server(debug=True)
