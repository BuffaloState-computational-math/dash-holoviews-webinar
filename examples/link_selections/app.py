# Load dataset
from plotly.data import iris
df = iris()

# Build HoloViews Dataset from Pandas DataFrame
import holoviews as hv
from holoviews.plotting.plotly.dash import to_dash
dataset = hv.Dataset(df)

# Build Scatter and Histogram HoloViews Elements, and side-by-side layout
scatter = hv.Scatter(dataset, kdims=["sepal_length"], vdims=["sepal_width"])
hist = hv.operation.histogram(
    dataset, dimension="petal_width", normed=False
)
row = scatter + hist

# Link selections across subplots
linked_row = hv.selection.link_selections(row)

# Build Dash app
import dash
app = dash.Dash(__name__)

# Build Dash components from HoloViews row Layout
components = to_dash(
    app, [linked_row], reset_button=True
)

# Build Dash layout
import dash_html_components as html
app.layout = html.Div(components.children)

if __name__ == "__main__":
    app.run_server(debug=True)
