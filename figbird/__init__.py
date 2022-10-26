from . import figures
from .schema import schema


@figures.Figure.new_if_none()
def line(*args, fig=None, **kwargs):
    return fig.add_line(*args, **kwargs)


@figures.Figure.new_if_none()
def scatter(*args, fig=None, **kwargs):
    return fig.add_scatter(*args, **kwargs)


@figures.Figure.new_if_none()
def bar(*args, fig=None, **kwargs):
    return fig.add_bar(*args, **kwargs)


@figures.Figure.new_if_none()
def envelope(*args, fig=None, **kwargs):
    return fig.add_envelope(*args, **kwargs)


@figures.Figure.new_if_none(schema=schema.figures.stripes)
def stripes(*args, fig=None, **kwargs):
    return fig.add_stripes(*args, **kwargs)
