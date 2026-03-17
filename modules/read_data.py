import pandas as pd
import rasterio
import numpy as np


def detect_columns(columns):
    """
    Robust column detection for real-world bathymetry datasets.
    """

    col_map = {col.lower(): col for col in columns}

    lat_candidates = ["lat", "latitude", "y"]
    lon_candidates = ["lon", "longitude", "long", "x"]
    depth_candidates = ["depth", "z", "elevation", "bathymetry"]

    lat_col = next((col_map[c] for c in col_map if c in lat_candidates), None)
    lon_col = next((col_map[c] for c in col_map if c in lon_candidates), None)
    depth_col = next((col_map[c] for c in col_map if c in depth_candidates), None)

    return lat_col, lon_col, depth_col


def load_data(file_path):

    # ---------- CSV ----------
    if file_path.endswith(".csv"):

        df = pd.read_csv(file_path)

        lat_col, lon_col, depth_col = detect_columns(df.columns)

        if not all([lat_col, lon_col, depth_col]):

            print("DEBUG: Available columns ->", list(df.columns))

            raise ValueError(
                f"Could not detect columns.\n"
                f"Found: {list(df.columns)}\n"
                f"Looking for lat/lon/depth variants"
            )

        return (
            df[lon_col].values,
            df[lat_col].values,
            df[depth_col].values
        )

    # ---------- GeoTIFF ----------
    elif file_path.endswith((".tif", ".tiff")):

        with rasterio.open(file_path) as src:

            data = src.read(1)
            transform = src.transform

            xs, ys, zs = [], [], []

            rows, cols = data.shape

            for r in range(rows):
                for c in range(cols):

                    z = data[r, c]

                    if np.isnan(z):
                        continue

                    x, y = rasterio.transform.xy(transform, r, c)

                    xs.append(x)
                    ys.append(y)
                    zs.append(z)

        return np.array(xs), np.array(ys), np.array(zs)

    else:
        raise ValueError("Unsupported file format")