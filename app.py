from flask import Flask, render_template, request, send_file
import os
import numpy as np
from PIL import Image

from modules.exporter import export_3d  # ✅ FIXED IMPORT
from config import UPLOAD_FOLDER, GRID_RESOLUTION
from modules.read_data import load_data
from modules.generate_map import generate_bathymetric_grid
from modules.visualize import create_plot


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ✅ GLOBAL STORAGE
grid_data = {}


# ---------------- MAIN ROUTE ---------------- #
@app.route("/", methods=["GET", "POST"])
def index():

    global grid_data

    plot_html = None

    if request.method == "POST":

        file = request.files["file"]

        if file:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)

            x, y, z = load_data(filepath)

            grid_x, grid_y, grid_z = generate_bathymetric_grid(
                x, y, z, GRID_RESOLUTION
            )

            # STORE DATA FOR EXPORT
            grid_data["x"] = grid_x
            grid_data["y"] = grid_y
            grid_data["z"] = grid_z

            plot_html = create_plot(grid_x, grid_y, grid_z)

    return render_template("index.html", plot=plot_html)


# ---------------- EXPORT PNG ---------------- #
@app.route("/export/png")
def export_png():

    global grid_data

    if not grid_data:
        return "❌ No data loaded"

    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, "map.png")

    z = np.nan_to_num(grid_data["z"])

    z_norm = (z - z.min()) / (z.max() - z.min()) * 255
    z_norm = z_norm.astype(np.uint8)

    image = Image.fromarray(z_norm)
    image.save(path)

    return send_file(path, as_attachment=True)


# ---------------- EXPORT 3D ---------------- #
@app.route("/export/3d/<file_type>")
def export_3d_route(file_type):

    global grid_data

    if not grid_data:
        return "❌ No data loaded"

    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"terrain.{file_type}"
    path = os.path.join(output_dir, filename)

    export_3d(
        grid_data["x"],
        grid_data["y"],
        grid_data["z"],
        path,
        file_type
    )

    return send_file(path, as_attachment=True)


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)