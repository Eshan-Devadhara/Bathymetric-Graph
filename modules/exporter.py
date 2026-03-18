import numpy as np
import trimesh


# ---------------- CREATE MESH ---------------- #
def create_mesh(grid_x, grid_y, grid_z):

    rows, cols = grid_z.shape

    vertices = []
    faces = []

    for i in range(rows):
        for j in range(cols):
            vertices.append([
                grid_x[i, j],
                grid_y[i, j],
                grid_z[i, j]
            ])

    vertices = np.array(vertices)

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

    return trimesh.Trimesh(vertices=vertices, faces=faces)


# ---------------- EXPORT 3D ---------------- #
def export_3d(grid_x, grid_y, grid_z, file_path, file_type):

    mesh = create_mesh(grid_x, grid_y, grid_z)

    if file_type == "obj":
        mesh.export(file_path)

    elif file_type == "stl":
        mesh.export(file_path)

    else:
        raise ValueError("Unsupported format")