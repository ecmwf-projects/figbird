import importlib

import plotly.graph_objects as go

from .schema import schema

__all__ = ["Figure"]


def _auto_trace(module_name=None):
    def decorator(method):
        def wrapper(fig, *args, row=None, col=None, secondary_y=None, **kwargs):
            name = method.__name__.replace("add_", "", 1)
            kwargs["fig"] = fig
            if module_name is None:
                module = importlib.import_module(
                    f"bluejay2.{fig.__class__.TRACE_MODULE}"
                )
            else:
                module = importlib.import_module(f"bluejay2.{module_name}")

            getattr(module, name)(*args, **kwargs)
            return fig

        return wrapper

    return decorator


class Figure(go.Figure):

    TRACE_MODULE = "plot"
    SCHEMA = schema.figure

    def __init__(self, *args, **kwargs):
        kwargs = self.SCHEMA._update_kwargs(kwargs)
        return super().__init__(*args, **kwargs)

    @classmethod
    def create_if_none(cls, function):
        def wrapper(*args, fig=None, **kwargs):
            if fig is None:
                fig = cls()
            return function(*args, fig=fig, **kwargs)

        return wrapper

    @_auto_trace()
    def add_line(self, *args, **kwargs):
        pass

    @_auto_trace("envelope")
    def add_envelope(self, *args, **kwargs):
        pass
