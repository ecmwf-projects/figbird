import numpy as np

colors = np.nditer(
    [
        [
            "#636EFA",
            "#EF553B",
            "#00CC96",
            "#AB63FA",
            "#FFA15A",
            "#19D3F3",
            "#FF6692",
            "#B6E880",
            "#FF97FF",
            "#FECB52",
        ]
    ],
)


def next_color():
    try:
        color = next(colors).item()
    except StopIteration:
        colors.reset()
        color = next_color()
    return color
