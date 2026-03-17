from flask import Flask, render_template, request
import os

from config import UPLOAD_FOLDER, GRID_RESOLUTION
from modules.read_data import load_data
from modules.generate_map import generate_bathymetric_grid
from modules.visualize import create_plot

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():

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

            plot_html = create_plot(grid_x, grid_y, grid_z)

    return render_template("index.html", plot=plot_html)


if __name__ == "__main__":
    app.run(debug=True)