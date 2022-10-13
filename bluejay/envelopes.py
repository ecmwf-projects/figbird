from . import Figure, plot
from .schema import schema


@Figure.create_if_none
@schema.envelope.apply()
# @inputs.polymorphic
def envelope(
    data,
    fig=None,
    envelope_dim=None,
    grouped_hoverlabel=False,
    showlegend="once",
    **kwargs,
):
    if not isinstance(data, (list, tuple)):
        data = _split_envelope(data, envelope_dim)

    if showlegend is not True:
        legendgroup = kwargs.get("name", f"trace {len(fig.data)+1}")
        kwargs["legendgroup"] = kwargs.get("legendgroup", legendgroup)

    turn_off_legend = False
    if showlegend == "once":
        showlegend_bottom = True
        showlegend_top = False
        turn_off_legend = True
    elif showlegend:
        showlegend_bottom = True
        showlegend_top = True
    else:
        showlegend_bottom = False
        showlegend_top = False

    for bottom, top in _iter_envelopes(data):
        plot.line(
            bottom,
            showlegend=showlegend_top,
            fig=fig,
            **_bound_kwargs(kwargs, final=top is None),
        )
        if top is not None:
            plot.line(
                top,
                showlegend=showlegend_bottom,
                fig=fig,
                fill="tonexty",
                **_bound_kwargs(kwargs),
            )
        if turn_off_legend:
            showlegend_bottom = False
            showlegend_top = False

    return fig


def _bound_kwargs(kwargs, final=False):
    kwargs = kwargs.copy()
    kwargs["line_width"] = 0 if not final else schema.line.line_width
    return kwargs


def _iter_envelopes(envelopes):
    for i in range(len(envelopes) // 2):
        yield envelopes[i], envelopes[-i - 1]
    if len(envelopes) % 2:
        yield envelopes[len(envelopes) // 2], None


def _split_envelope(data, envelope_dim=None):
    if envelope_dim is None:
        raise TypeError("'envelope_dim' arg required for non-list data")
    data = [data.isel(**{envelope_dim: i}) for i in range(len(data[envelope_dim]))]
    return data
