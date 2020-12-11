## Dash Holoviews Webinar Examples
This repository contains examples for the [Dash HoloViews webinar](https://go.plotly.com/dash-holoviews) on December 16th. 

## Mapbox Token
Some of these examples require a mapbox token that can be created from a free mapbox account at  https://www.mapbox.com/.

To run these apps, you must **either**:
 - Create an environment variable named `MAPBOX_TOKEN` that is set to your token string.
 - Create a file named `.mapbox` in the top-level project directory containing your token.
 
## Setup environment
Set up the app environment in a fresh virtual environment with

```
pip install -r requirements.txt
```

## Run the Apps
The individual examples are located under the top-level `examples/` directory.
Run an example by calling:

```
python examples/{example_name}/app.py
```

For example, to run the `link_selections` example, run:

```
python examples/link_selections/app.py
```
