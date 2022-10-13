import plotly.graph_objects as go

from . import Figure, inputs, layout
from .schema import schema


@Figure.create_if_none
@schema.line.apply()
@inputs.polymorphic
@layout.update
def line(*args, fig=None, **kwargs):
    fig.add_trace(go.Scatter(*args, **kwargs))
    return fig
