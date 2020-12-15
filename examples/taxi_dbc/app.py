# Dash and Plotly import
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.io as pio
from plotly import colors

# HoloViews imports
import holoviews as hv
from holoviews.operation import histogram
from holoviews.operation.datashader import datashade
from holoviews.plotting.plotly.dash import to_dash
from holoviews.selection import link_selections

# Other imports
import pandas as pd
from download_dataset import download_dataset
from mapbox_token import get_mapbox_token

# Set default plotly template
pio.templates.default = "plotly_white"

# Download and load Taxi dataset
df = pd.read_parquet(download_dataset())
ds = hv.Dataset(df)

# # Uncomment for CUDF support
# import cudf
# ds = hv.Dataset(cudf.from_pandas(df))

# Add more descriptive axis labels
ds = ds.redim.label(fare_amount="Fare Amount")

# Create Datashaded points Element
points = hv.Points(ds, ["dropoff_x", "dropoff_y"])
shaded = datashade(points, cmap=colors.sequential.Plasma)

# Create Tiles Element dispaying a mapbox light theme map
tiles = hv.Tiles().opts(
    mapboxstyle="light", accesstoken=get_mapbox_token(),
    height=500, width=500, padding=0
)

# Create overlay of datashaded Scatter element on top of map
map_overlay = tiles * shaded

# Create Histogram Element
hist = histogram(
    ds, dimension="fare_amount", normed=False, num_bins=20, bin_range=(0, 30.0)
).opts(color=colors.qualitative.Plotly[0], height=500)

# Build selection linking object that can be reused to link across plots
lnk_sel = link_selections.instance()

# Link selections across map overlay and histogram
linked_map_overlay = lnk_sel(map_overlay)
linked_hist = lnk_sel(hist)

# Use plot hook to set the default histogram drag mode to box selection
def set_dragmode(plot, element):
    fig = plot.state
    fig["layout"]["dragmode"] = "select"
    fig["layout"]["selectdirection"] = "h"
linked_hist.opts(hv.opts.Histogram(hooks=[set_dragmode]))

# Set plot margins, ordered (left, bottom, right, top)
linked_hist.opts(margins=(60, 40, 30, 30))
linked_map_overlay.opts(margins=(30, 30, 30, 30))

# Build Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Build Dash components from multiple HoloViews Elements
components = to_dash(
    app, [linked_map_overlay, linked_hist], reset_button=True, button_class=dbc.Button,
)

# Build Dash layout using Dash Bootstrap Components
app.layout = dbc.Container([
    html.H1("NYC Taxi Demo", style={"padding-top": 40}),
    html.H3("Crossfiltering 10 million trips with Dash, Datashader, and HoloViews"),
    html.Hr(),
    dbc.Row([
        dbc.Col(children=[dbc.Card([
            dbc.CardHeader("Drop off locations"),
            dbc.CardBody(children=[
                components.graphs[0],
            ])])]),
        dbc.Col(children=[dbc.Card([
            dbc.CardHeader("Fare Amount"),
            dbc.CardBody(children=[
                components.graphs[1]
            ])])])
    ]),
    html.Div(style={"margin-top": 10}, children=components.resets[0]),
    components.store,
])

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
