import numpy as np
import trimesh
from PIL import Image
import os


# ---------------- 3D EXPORT ---------------- #
def export_to_obj(grid_x, grid_y, grid_z, output_path):

    rows, cols = grid_z.shape

    vertices = []
    faces = []

    # Create vertices
    for i in range(rows):
        for j in range(cols):
            vertices.append([
                grid_x[i, j],
                grid_y[i, j],
                grid_z[i, j]
            ])

    vertices = np.array(vertices)

    # Create faces (triangles)
    def index(i, j):
        return i * cols + j

    for i in range(rows - 1):
        for j in range(cols - 1):

            v1 = index(i, j)
            v2 = index(i, j + 1)
            v3 = index(i + 1, j)
            v4 = index(i + 1, j + 1)

            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])

    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    mesh.export(output_path)


# ---------------- 2D IMAGE EXPORT ---------------- #
def export_to_png(grid_z, output_path):

    z = np.nan_to_num(grid_z)

    # Normalize 0–255
    z_norm = (z - z.min()) / (z.max() - z.min()) * 255
    z_norm = z_norm.astype(np.uint8)

    image = Image.fromarray(z_norm)

    image.save(output_path)