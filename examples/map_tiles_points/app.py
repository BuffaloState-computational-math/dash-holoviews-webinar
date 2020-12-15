# Load geographic dataset and convert from lon/lat to web-mercator easting/northing coordinates
from plotly.data import carshare
import holoviews as hv
df = carshare()
df["easting"], df["northing"] = hv.Tiles.lon_lat_to_easting_northing(
    df["centroid_lon"], df["centroid_lat"]
)

# Build Scatter element and overlay on top of HoloViews map Tiles Element
from holoviews.plotting.plotly.dash import to_dash
from holoviews.element.tiles import CartoDark
points = hv.Scatter(df, "easting", "northing").opts(color="crimson")
tiles = CartoDark()
overlay = tiles * points

# Build Dash app
import dash
app = dash.Dash(__name__)
layout = app.layout

# Build Dash components from HoloViews row Layout
components = to_dash(app, [overlay])

# Build Dash layout
import dash_html_components as html
app.layout = html.Div(
    components.children
)

if __name__ == '__main__':
    app.run_server(debug=True)
