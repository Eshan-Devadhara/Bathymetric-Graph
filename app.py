from flask import Flask, render_template, request, send_file, jsonify
import os
import uuid
import numpy as np
from PIL import Image

from modules.exporter import export_3d
from config import UPLOAD_FOLDER, GRID_RESOLUTION
from modules.read_data import load_data
from modules.generate_map import generate_bathymetric_grid

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Dictionary to map unique session IDs to their loaded grid data
grid_sessions = {}

# Ensure folders exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs("data/output", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")

    file = request.files.get("file")
    if not file or file.filename == "":
        return jsonify({"error": "No file uploaded"}), 400

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    
    try:
        file.save(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    try:
        x, y, z = load_data(filepath)
        grid_x, grid_y, grid_z = generate_bathymetric_grid(x, y, z, GRID_RESOLUTION)
    except Exception as e:
        return jsonify({"error": f"Failed to process data: {str(e)}"}), 400

    session_id = str(uuid.uuid4())
    grid_sessions[session_id] = {
        "x": grid_x,
        "y": grid_y,
        "z": grid_z
    }

    return jsonify({
        "session_id": session_id,
        "x": grid_x.tolist(),
        "y": grid_y.tolist(),
        "z": grid_z.tolist()
    })

@app.route("/export/png/<session_id>")
def export_png(session_id):
    if session_id not in grid_sessions:
        return "❌ Data session expired or invalid", 404

    grid_data = grid_sessions[session_id]
    output_dir = "data/output"
    path = os.path.join(output_dir, f"map_{session_id}.png")

    z = np.nan_to_num(grid_data["z"])
    z_norm = (z - z.min()) / (z.max() - z.min()) * 255
    z_norm = z_norm.astype(np.uint8)

    image = Image.fromarray(z_norm)
    image.save(path)

    return send_file(path, as_attachment=True, download_name="bathymetric_map.png")

@app.route("/export/3d/<session_id>/<file_type>")
def export_3d_route(session_id, file_type):
    if session_id not in grid_sessions:
        return "❌ Data session expired or invalid", 404
        
    if file_type not in ["obj", "stl"]:
        return "❌ Invalid file type", 400

    grid_data = grid_sessions[session_id]
    output_dir = "data/output"
    filename = f"terrain_{session_id}.{file_type}"
    path = os.path.join(output_dir, filename)

    export_3d(grid_data["x"], grid_data["y"], grid_data["z"], path, file_type)

    return send_file(path, as_attachment=True, download_name=f"terrain.{file_type}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)