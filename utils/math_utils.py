import numpy as np

def create_grid(x, y, resolution):
    """
    Create interpolation grid
    """

    xi = np.linspace(min(x), max(x), 100)
    yi = np.linspace(min(y), max(y), 100)

    grid_x, grid_y = np.meshgrid(xi, yi)

    return grid_x, grid_y