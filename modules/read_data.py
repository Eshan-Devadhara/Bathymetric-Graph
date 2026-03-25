import pandas as pd
import numpy as np
import rasterio
import xarray as xr
import os


def load_data(filepath):

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".csv":
        return load_csv(filepath)

    elif ext in [".tif", ".tiff"]:
        return load_geotiff(filepath)

    elif ext in [".nc"]:
        return load_netcdf(filepath)

    elif ext in [".asc"]:
        return load_ascii(filepath)

    else:
        raise ValueError(f"Unsupported file format: {ext}")


# ---------------- CSV ---------------- #
def load_csv(filepath):

    df = pd.read_csv(filepath)

    cols = [c.lower() for c in df.columns]

    # Flexible detection
    if "lat" in cols and "lon" in cols:
        lat = df[df.columns[cols.index("lat")]]
        lon = df[df.columns[cols.index("lon")]]
    elif "lat" in cols and "long" in cols:
        lat = df[df.columns[cols.index("lat")]]
        lon = df[df.columns[cols.index("long")]]
    elif "latitude" in cols and "longitude" in cols:
        lat = df[df.columns[cols.index("latitude")]]
        lon = df[df.columns[cols.index("longitude")]]
    elif "y" in cols and "x" in cols:
        lat = df[df.columns[cols.index("y")]]
        lon = df[df.columns[cols.index("x")]]
    else:
        raise ValueError(f"Could not detect coordinates. Found: {df.columns}")

    # Depth detection
    if "depth" in cols:
        z = df[df.columns[cols.index("depth")]]
    elif "z" in cols:
        z = df[df.columns[cols.index("z")]]
    else:
        raise ValueError("Depth column not found")

    return lon.values, lat.values, z.values


# ---------------- GeoTIFF ---------------- #
def load_geotiff(filepath):

    with rasterio.open(filepath) as src:
        z = src.read(1)

        transform = src.transform

        rows, cols = z.shape

        xs = np.arange(cols)
        ys = np.arange(rows)

        xs, ys = np.meshgrid(xs, ys)

        lon, lat = rasterio.transform.xy(transform, ys, xs)

        return np.array(lon).flatten(), np.array(lat).flatten(), z.flatten()


# ---------------- NetCDF ---------------- #
def load_netcdf(filepath):

    ds = xr.open_dataset(filepath)

    # Try to detect variables
    possible_z = list(ds.data_vars.keys())[0]
    z = ds[possible_z]

    lat = ds.coords.get("lat") or ds.coords.get("latitude")
    lon = ds.coords.get("lon") or ds.coords.get("longitude")

    if lat is None or lon is None:
        raise ValueError("NetCDF missing lat/lon")

    lon_grid, lat_grid = np.meshgrid(lon.values, lat.values)

    return lon_grid.flatten(), lat_grid.flatten(), z.values.flatten()


# ---------------- ESRI ASCII ---------------- #
def load_ascii(filepath):

    with rasterio.open(filepath) as src:
        z = src.read(1)

        transform = src.transform

        rows, cols = z.shape

        xs = np.arange(cols)
        ys = np.arange(rows)

        xs, ys = np.meshgrid(xs, ys)

        lon, lat = rasterio.transform.xy(transform, ys, xs)

        return np.array(lon).flatten(), np.array(lat).flatten(), z.flatten()