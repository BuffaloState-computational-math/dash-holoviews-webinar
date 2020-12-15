# Load dataset
from plotly.data import iris
df = iris()

# Build HoloViews Dataset from Pandas DataFrame
import holoviews as hv
dataset = hv.Dataset(df)

# Build HoloViews Elements
scatter = hv.Scatter(dataset, kdims=["sepal_length"], vdims=["sepal_width"])
hist = hv.operation.histogram(
    dataset, dimension="petal_width", normed=False
)

# Build side-by-side subplot of scatter and histogram
row = scatter + hist

# Build Dash app
import dash
app = dash.Dash(__name__)

# Build Dash components from HoloViews row Layout
from holoviews.plotting.plotly.dash import to_dash
components = to_dash(app, [row])

# Build Dash layout
import dash_html_components as html
app.layout = html.Div(components.children)

if __name__ == "__main__":
    app.run_server(debug=True)
