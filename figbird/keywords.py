def get(key, kwargs):
    if key in kwargs:
        value = kwargs[key]
    else:
        magic_key, *child_key = key.split("_")
        child_key = "_".join(child_key)
        value = kwargs.get(magic_key, dict()).get(child_key)
    return value
