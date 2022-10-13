def update(function):
    def wrapper(*args, fig, _update_layout=None, **kwargs):
        if _update_layout is not None:
            fig.update_layout(_update_layout)
        return function(*args, fig=fig, **kwargs)

    return wrapper
