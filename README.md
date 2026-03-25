# Bathymetric GIS Viewer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Plotly](https://img.shields.io/badge/Plotly-interactive-orange.svg)](https://plotly.com/python/)

An interactive web application for processing and visualizing bathymetric (seabed depth) data. Upload CSV or GeoTIFF files containing latitude, longitude, and depth points to generate publication-ready 2D contour maps and 3D surface visualizations.

## Features

- **Robust Backend Error Handling**: Utilizes UUID session-based state management to safely manage active datasets, prevent multi-upload conflicts, and provide detailed format error logging.
- **Multiple Supported Formats**: Automatically detects various combinations of column names (e.g., `lat`/`latitude`/`y`, `lon`/`longitude`/`long`/`x`, and `depth`/`z`) in CSV files, and natively supports GeoTIFFs.
- **Dual Visualization Dashboard**: Renders 2D contour plots and interactive 3D surface maps side-by-side using the Plotly library.
- **Modern User Interface**: Features a clean, dark-mode design with clear status indicators and responsive layout elements.
- **Automated Processing**: Selecting a file immediately initiates background SciPy interpolation, streamlining the user workflow.
- **Production Ready**: Successfully tested with real-world datasets, including Geelong bathymetric contours.

## Quick Start

```bash
# Clone the repository and install dependencies
pip install -r requirements.txt

# Run the development server
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

## Usage

1. **Upload**: Click the **Upload Dataset** button and select a CSV or GeoTIFF data file. Processing will begin automatically.
2. **Auto-process**: The system will detect coordinate and depth columns, clean the raw data, and generate an interpolated grid. A progress indicator is displayed during computation.
3. **View Results**: Upon completion, the interface displays the 2D contour map alongside the 3D rotatable surface plot.
4. **Export**: Use the provided controls in the sidebar to export the 2D map as a PNG image, or download the 3D surface model as `.obj` or `.stl` files.

### Supported Data Formats

**CSV**: Columns containing `lat/latitude/y`, `lon/longitude/x`, and `depth/z/elevation/bathymetry` values.
```
long,lat,depth
144.665, -38.313, -5.2
...
```

**GeoTIFF**: Standard raster bathymetry with an embedded Coordinate Reference System (CRS).

## Project Structure

```
Bathymetric Graph/
├── app.py                 # Flask application and main routing
├── config.py              # Configuration and path settings
├── requirements.txt       # Python dependencies
├── data/
│   ├── raw/              # Temporary storage for uploaded files
│   ├── preprocessed/     # Storage for cleaned CSVs
│   └── output/           # Directory for generated grids and exports
├── modules/
│   ├── read_data.py      # File parsing logic for CSV/GeoTIFF
│   ├── preprocess.py     # Data cleaning algorithms
│   ├── generate_map.py   # Grid interpolation using SciPy
│   └── visualize.py      # Plotly rendering integration
├── static/
│   ├── app.js           # Client-side logic and API requests
│   └── style.css        # Application styling Definitions
├── templates/
│   └── index.html       # Primary HTML template
└── utils/
    ├── file_utils.py    # General file I/O operations
    └── math_utils.py    # Grid and mathematical helper functions
```

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with python (with auto-reload enabled in debug mode)
python app.py

# Alternatively, run using the Flask CLI
flask --app app.py run --debug
```

**Customization Guidelines**:
- Modify `config.py` → `GRID_RESOLUTION` to adjust the resolution of the interpolated grid.
- Adjust `modules/visualize.py` to implement custom colorscales.
- Extend `modules/read_data.py` to add support for new proprietary data formats.

## Example Data

Testing can be performed using the included [Geelong bathymetric contours](data/raw/bathymetric-contours-city-of-greater-geelong.csv) dataset.

## Contributing

1. Fork the repository and create a Pull Request.
2. Add necessary tests within the `tests/` directory.
3. Ensure all Python code adheres to PEP8 styling standards.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
