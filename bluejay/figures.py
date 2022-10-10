import plotly.graph_objects as go

from .schema import schema


@schema.figure.apply()
def figure(*args, **kwargs):
    return go.Figure(*args, **kwargs)


def heatmap_figure(*args, **kwargs):
    kwargs.update(
        layout={
            "xaxis": {
                "zeroline": False,
                "showline": False,
                "showgrid": False,
                "fixedrange": True,
                "showticklabels": False,
                "ticklabelmode": "period",
            },
            "yaxis": {
                "zeroline": False,
                "showline": False,
                "showgrid": False,
                "fixedrange": True,
                "showticklabels": False,
            },
            "hoverdistance": -1,
            "height": 300,
        },
    )
    return figure(*args, **kwargs)
