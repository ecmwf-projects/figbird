import collections.abc


class Schema(dict):
    def __init__(self, **kwargs):
        self.update(**kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, Schema):
            value = Schema(**value)
        try:
            self[key] = value
        except:  # noqa: E722
            raise AttributeError(key)
        else:
            object.__setattr__(self, key, value)

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def apply(self):
        def decorator(function):
            def wrapper(*args, **kwargs):
                return function(*args, **_recursive_dict_update(self.to_dict(), kwargs))

            return wrapper

        return decorator

    def to_dict(self):
        d = dict()
        for key, value in self.items():
            if isinstance(value, type(self)):
                value = value.to_dict()
            d[key] = value
        return d

    def set(self, **kwargs):
        return _set(self, **kwargs)

    def get_magic(self, key):
        if key in self:
            return self[key]
        else:
            magic_key, *kwarg = key.split("_")
            if magic_key in self:
                return self[magic_key]["_".join(kwarg)]


class _set:
    def __init__(self, schema, **kwargs):
        self.schema = schema
        self.old_kwargs = {key: self.schema.get(key) for key in kwargs}
        self.new_kwargs = [key for key in kwargs if key not in self.schema]
        self.schema.update(**kwargs)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.schema.update(**self.old_kwargs)
        for key in self.new_kwargs:
            self.schema.pop(key, None)


def _recursive_dict_update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = _recursive_dict_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


schema = Schema(
    **{
        "settings": {
            "hover_precision": ".1f",
            "line": {
                # TODO: Make this work!
                "marker_threshold": 60,
            },
        },
        "figure": {
            "layout": {
                "plot_bgcolor": "white",
                "xaxis": {
                    "zeroline": False,
                    "showline": False,
                    "showgrid": True,
                    "gridwidth": 1,
                    "gridcolor": "#EEEEEE",
                },
                "yaxis": {
                    "zeroline": False,
                    "showline": True,
                    "linecolor": "black",
                    "showgrid": False,
                },
                "hovermode": "x",
            },
        },
        "line": {
            "line": {
                "width": 2,
                "shape": "linear",
            },
            "marker": {
                "size": 6,
                "line_width": 2,
                "line_color": "white",
            },
        },
        "stripes": {
            "showscale": False,
        },
        "envelope": {
            "line": {
                "width": 0,
                "shape": "linear",
            },
            "mode": "lines",
        },
    }
)
