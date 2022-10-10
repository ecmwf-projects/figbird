import plotly.graph_objects as go

from . import inputs
from .schema import schema


@schema.stripes.apply()
@inputs.polymorphic_input
def stripes(*args, diverging=True, divergence_point=0, **kwargs):
    z = kwargs.pop("y")

    zmin = min(z)
    zmax = max(z)

    if diverging:
        abs_zmax = max(zmax - divergence_point, divergence_point - zmin)
        zmax = divergence_point + abs_zmax
        zmin = divergence_point - abs_zmax
        kwargs["colorscale"] = kwargs.pop("colorscale", "RdBu_r")

    return go.Heatmap(*args, y=[1] * len(z), z=z, zmin=zmin, zmax=zmax, **kwargs)
