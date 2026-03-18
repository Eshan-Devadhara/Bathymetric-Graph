from flask import Flask, render_template, request
import os

from modules.exporter import export_to_obj, export_to_png
from config import UPLOAD_FOLDER, GRID_RESOLUTION
from modules.read_data import load_data
from modules.generate_map import generate_bathymetric_grid
from modules.visualize import create_plot


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ✅ GLOBAL STORAGE (for export)
grid_data = {}


# ---------------- MAIN ROUTE ---------------- #
@app.route("/", methods=["GET", "POST"])
def index():

    global grid_data  # IMPORTANT

    plot_html = None

    if request.method == "POST":

        file = request.files["file"]

        if file:

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)

            # Load data
            x, y, z = load_data(filepath)

            # Generate grid
            grid_x, grid_y, grid_z = generate_bathymetric_grid(
                x, y, z, GRID_RESOLUTION
            )

            # ✅ Store for export
            grid_data["x"] = grid_x
            grid_data["y"] = grid_y
            grid_data["z"] = grid_z

            # Create visualization
            plot_html = create_plot(grid_x, grid_y, grid_z)

    return render_template("index.html", plot=plot_html)


# ---------------- EXPORT 3D ---------------- #
@app.route("/export/obj")
def export_obj():

    global grid_data

    if not grid_data:
        return "❌ No data loaded. Please upload a dataset first."

    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, "terrain.obj")

    export_to_obj(
        grid_data["x"],
        grid_data["y"],
        grid_data["z"],
        path
    )

    return f"✅ 3D Model saved at {path}"


# ---------------- EXPORT 2D ---------------- #
@app.route("/export/png")
def export_png():

    global grid_data

    if not grid_data:
        return "❌ No data loaded. Please upload a dataset first."

    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, "map.png")

    export_to_png(
        grid_data["z"],
        path
    )

    return f"✅ Image saved at {path}"


# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)