import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_plot(grid_x, grid_y, grid_z):

    grid_z = np.nan_to_num(grid_z)

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "contour"}, {"type": "surface"}]],
        subplot_titles=("2D Map", "3D Seabed")
    )

    # 2D
    fig.add_trace(
        go.Contour(
            x=grid_x[0],
            y=grid_y[:, 0],
            z=grid_z,
            colorscale="Viridis"
        ),
        row=1,
        col=1
    )

    # 3D
    fig.add_trace(
        go.Surface(
            x=grid_x,
            y=grid_y,
            z=grid_z,
            colorscale="Viridis"
        ),
        row=1,
        col=2
    )

    fig.update_layout(height=600, width=1000)

    return fig.to_html(full_html=False)