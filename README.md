# 🌊 Bathymetric GIS Viewer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Plotly](https://img.shields.io/badge/Plotly-interactive-orange.svg)](https://plotly.com/python/)

**Interactive web application for processing and visualizing bathymetric (seabed depth) data.** Upload CSV or GeoTIFF files with lat/lon/depth points and instantly generate publication-ready 2D contour maps and 3D surface visualizations.

## ✨ Features

- **📁 Multiple Formats**: CSV (auto-detect columns) & GeoTIFF
- **🧠 Smart Processing**: Robust column detection (lat/lon/depth variants), data cleaning, grid interpolation
- **📊 Dual Visualization**: 2D contour plots + interactive 3D surfaces (Plotly)
- **🎨 Modern UI**: Dark GIS-style interface with layers panel & status bar
- **⚡ Fast**: SciPy interpolation, optimized for large datasets
- **🌍 Real Data Ready**: Tested with Geelong bathymetric contours

## 🚀 Quick Start

```bash
# Clone & install
pip install -r requirements.txt

# Run development server
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## 📝 Usage

1. **Upload** CSV or GeoTIFF file via \"Load Layer\" button
2. **Auto-process**: Columns detected, data cleaned, grid generated (0.001° resolution)
3. **View Results**: Side-by-side 2D contour map + 3D rotatable surface plot
4. **Layer Management**: Multiple layers in sidebar

### Supported Data Formats

**CSV**: Columns containing `lat/latitude/y`, `lon/longitude/x`, `depth/z/elevation/bathymetry`
```
long,lat,depth
144.665, -38.313, -5.2
...
```

**GeoTIFF**: Standard raster bathymetry with CRS

## 🏗️ Project Structure

```
Bathymetric Graph/
├── app.py                 # Flask app & main route
├── config.py              # Paths & settings
├── requirements.txt       # Dependencies
├── data/
│   ├── raw/              # Uploaded files
│   ├── preprocessed/     # Cleaned CSVs
│   └── output/           # Generated grids
├── modules/
│   ├── read_data.py      # CSV/GeoTIFF parsing
│   ├── preprocess.py     # Data cleaning
│   ├── generate_map.py   # Grid interpolation
│   └── visualize.py      # Plotly plots
├── static/
│   ├── app.js           # File upload & UI logic
│   └── style.css        # Dark GIS theme
├── templates/
│   └── index.html       # Main UI template
└── utils/
    ├── file_utils.py    # File I/O
    └── math_utils.py    # Grid helpers
```

## 📱 Demo Screenshot

*(Upload a file to see interactive plots in action)*

## 🔧 Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run with auto-reload
python app.py

# Or with Flask CLI
flask --app app.py run --debug
```

**Customization**:
- Edit `config.py` → `GRID_RESOLUTION` for finer/coarser grids
- Modify `modules/visualize.py` for custom colorscales
- Extend `modules/read_data.py` for new formats

## 📊 Example Data

Test with included [Geelong bathymetric contours](data/raw/bathymetric-contours-city-of-greater-geelong.csv)

## 🤝 Contributing

1. Fork & create PR
2. Add tests in `tests/`
3. Follow PEP8 style

## 📄 License

MIT License - see [LICENSE](LICENSE) *(create if needed)*

---

**Built with ❤️ for oceanographers, GIS analysts, and seabed explorers.**

