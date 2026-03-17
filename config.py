import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Existing
DATA_DIR = os.path.join(BASE_DIR, "data")

# New for Flask
UPLOAD_FOLDER = os.path.join(DATA_DIR, "raw")

ALLOWED_EXTENSIONS = {"csv", "tif", "tiff"}

GRID_RESOLUTION = 0.001