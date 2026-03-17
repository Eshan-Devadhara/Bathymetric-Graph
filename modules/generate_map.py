import numpy as np
from scipy.interpolate import griddata


def generate_bathymetric_grid(x, y, z, resolution=0.001):

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    xi = np.arange(xmin, xmax, resolution)
    yi = np.arange(ymin, ymax, resolution)

    if len(xi) < 2:
        xi = np.linspace(xmin, xmax + resolution, 2)

    if len(yi) < 2:
        yi = np.linspace(ymin, ymax + resolution, 2)

    grid_x, grid_y = np.meshgrid(xi, yi)

    grid_z = griddata(
        (x, y),
        z,
        (grid_x, grid_y),
        method="nearest"
    )

    return grid_x, grid_y, grid_z