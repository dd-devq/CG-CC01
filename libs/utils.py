import numpy as np
from sympy import *
import math
from OpenGL.GL import *
from PIL import Image

# GL_TRIANGLES


def calculate_vertex_normals(vertices, indices):
    normals = np.zeros(vertices.shape, dtype=np.float32)

    for i in range(0, len(indices), 3):
        i1, i2, i3 = indices[i:i+3]
        v1, v2, v3 = vertices[i1], vertices[i2], vertices[i3]
        normal = np.cross(v2 - v1, v3 - v1)
        normal /= np.linalg.norm(normal)
        normal = np.nan_to_num(normal, nan=0)
        normals[i1] += normal
        normals[i2] += normal
        normals[i3] += normal

    normals /= np.linalg.norm(normals, axis=1)[:, np.newaxis]
    normal = np.nan_to_num(normal, nan=0)

    return normals

# GL_TRIANGLE_STRIPS


def calculate_vertex_normals_2(vertices, indices):
    normals = np.zeros(vertices.shape, dtype=np.float32)

    for i in range(0, len(indices) - 2):
        i1, i2, i3 = indices[i:i+3]
        v1, v2, v3 = vertices[i1], vertices[i2], vertices[i3]
        normal = np.cross(v2 - v1, v3 - v1)
        normal /= np.linalg.norm(normal)
        normals[i1] += normal
        normals[i2] += normal
        normals[i3] += normal

    normals /= np.linalg.norm(normals, axis=1)[:, np.newaxis]
    return normals


# ------------ Sphere 1 ------------


def sphere_1(radius, num_segments):
    vertices, indices = [], []
    for i in range(num_segments + 1):
        theta1 = i * math.pi / num_segments
        sin_theta1 = math.sin(theta1)
        cos_theta1 = math.cos(theta1)

        for j in range(num_segments + 1):
            phi1 = j * 2 * math.pi / num_segments
            sin_phi1 = math.sin(phi1)
            cos_phi1 = math.cos(phi1)
            x = radius * sin_theta1 * cos_phi1
            y = radius * sin_theta1 * sin_phi1
            z = radius * cos_theta1

            vertices.append([x, y, z])

            if i < num_segments and j < num_segments:
                first = (i * (num_segments + 1)) + j
                second = first + num_segments + 1
                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

# ------------ Sphere 2 ------------


def create_tetrahedron():
    # define vertices of a regular tetrahedron
    vertices = [[0, 0, 1],
                [0.8165, 0, -0.5],
                [-0.4082, 0.7071, -0.5],
                [-0.4082, -0.7071, -0.5],
                ]

    # define indices of the tetrahedron's faces
    indices = [0, 1, 2, 0, 2, 3, 0, 3, 1, 1, 3, 2]

    return vertices, indices


def normalize(vec):
    # normalize a 3D vector
    length = math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)
    return [vec[0]/length, vec[1]/length, vec[2]/length]


def subdivide(face, vertices):
    # subdivide a face into smaller triangles
    v1 = vertices[face[0]]
    v2 = vertices[face[1]]
    v3 = vertices[face[2]]
    v12 = normalize([(v1[0]+v2[0])/2, (v1[1]+v2[1])/2, (v1[2]+v2[2])/2])
    v23 = normalize([(v2[0]+v3[0])/2, (v2[1]+v3[1])/2, (v2[2]+v3[2])/2])
    v31 = normalize([(v3[0]+v1[0])/2, (v3[1]+v1[1])/2, (v3[2]+v1[2])/2])
    vertices.append(v12)
    vertices.append(v23)
    vertices.append(v31)
    i1 = len(vertices)-3
    i2 = len(vertices)-2
    i3 = len(vertices)-1
    indices = [face[0], i1, i3, face[1], i2, i1, face[2], i3, i2, i1, i2, i3]
    return indices


def sphere_2(num_subdivisions):

    vertices, indices = create_tetrahedron()
    for i in range(num_subdivisions):
        new_indices = []
        for j in range(0, len(indices), 3):
            face = [indices[j], indices[j+1], indices[j+2]]

            new_indices += subdivide(face, vertices)
        indices = new_indices

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


# ------------ Cylinder ------------

def cylinder(radius, height, sides):
    vertices, indices, color = [], [], []
    color_step = 0
    for i in range(sides):
        theta = 2 * np.pi * i / sides
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        vertices += [[x, y, -height / 2], [x, y, height / 2]]
        color += [1, 0, 0]
        color += [1, 1, 0]

    color += [1, 0, 0]
    color += [1, 1, 0]

    for i in range(0, len(vertices) - 1, 2):
        if i == len(vertices) - 2:
            indices += [i, i + 1, 1, i, 0, 1]
        else:
            indices += [i, i + 1, i + 3, i, i + 2, i + 3]

    # Bottom Indices
    vertices += [[0, 0, -height / 2]]
    for i in range(len(vertices) - 2):
        if (i % 2 == 0) and i == len(vertices) - 3:
            indices += [i]
            indices += [len(vertices) - 1]
            indices += [0]
        elif (i % 2 == 0):
            indices += [i]
            indices += [len(vertices) - 1]
            indices += [i + 2]

    # Top Indices
    vertices += [[0, 0, height/2]]
    for i in range(len(vertices) - 2):
        if (i % 2 != 0) and i == len(vertices) - 3:
            indices += [i]
            indices += [len(vertices) - 1]
            indices += [1]
        elif (i % 2 != 0):
            indices += [i]
            indices += [len(vertices) - 1]
            indices += [i + 2]

    # Convert vertex and index data to NumPy arrays
    vertices = np.array(vertices, dtype=np.float32)
    color = np.array(color, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    return vertices, indices, color

# ------------ Frustum ------------


def frustum(radius_top, radius_bottom, height, sides=4):
    vertices, indices, color = [], [], []
    color_step = 0
    for i in range(sides):
        theta = 2 * np.pi * i / sides
        x1 = radius_bottom * np.cos(theta)
        y1 = radius_bottom * np.sin(theta)
        x2 = radius_top * np.cos(theta)
        y2 = radius_top * np.sin(theta)
        vertices += [[x1, y1, -height / 2], [x2, y2, height / 2]]
        color += [1, 0, 0]
        color += [1, 1, 0]

    color += [1, 0, 0]
    color += [1, 1, 0]

    for i in range(0, len(vertices) - 1, 2):
        if i == len(vertices) - 2:
            indices += [i, i + 1, 1, i, 0, 1]
        else:
            indices += [i, i + 1, i + 3, i, i + 2, i + 3]

    # Bottom Indices
    vertices += [[0, 0, -height / 2]]
    for i in range(len(vertices) - 2):
        if (i % 2 == 0) and i == len(vertices) - 3:
            indices += [i]
            indices += [len(vertices) - 1]
            indices += [0]
        elif (i % 2 == 0):
            indices += [i]
            indices += [len(vertices) - 1]
            indices += [i + 2]

    # Top Indices
    vertices += [[0, 0, height/2]]
    for i in range(len(vertices) - 2):
        if (i % 2 != 0) and i == len(vertices) - 3:
            indices += [i]
            indices += [len(vertices) - 1]
            indices += [1]
        elif (i % 2 != 0):
            indices += [i]
            indices += [len(vertices) - 1]
            indices += [i + 2]

    # Convert vertex and index data to NumPy arrays
    vertices = np.array(vertices, dtype=np.float32)
    color = np.array(color, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    return vertices, indices, color


# ------------ Cone ------------

def cone(num_segments, height, radius):
    vertices, indices, color = [], [], []
    angle_step = 2.0 * np.pi / num_segments

    vertices.append([0.0, height, 0.0])
    color.append([1, 1, 0])

    for i in range(num_segments):
        angle = i * angle_step
        x = radius * np.cos(angle)
        y = -height
        z = radius * np.sin(angle)
        vertices.append([x, y, z])
        color.append([1, 0, 0])
    color.append([1, 0, 0])

    for i in range(num_segments - 1):
        indices.append(i + 1)
        indices.append(0)
        indices.append(i + 2)

    indices.append(num_segments)
    indices.append(0)
    indices.append(1)
    vertices.append([0.0, -height, 0.0])

    for i in range(1, len(vertices) - 1):
        if i == len(vertices) - 2:
            indices.append(i)
            indices.append(len(vertices) - 1)
            indices.append(1)
        else:
            indices.append(i)
            indices.append(len(vertices) - 1)
            indices.append(i + 1)

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    color = np.array(color, dtype=np.float32)
    return vertices, indices, color


# ------------ Ellipsoid ------------

def ellipsoid(radius1, radius2, radius3, num_segments):
    vertices = []
    indices = []
    for i in range(num_segments + 1):
        theta1 = i * math.pi / num_segments
        sin_theta1 = math.sin(theta1)
        cos_theta1 = math.cos(theta1)

        for j in range(num_segments + 1):
            phi1 = j * 2 * math.pi / num_segments
            sin_phi1 = math.sin(phi1)
            cos_phi1 = math.cos(phi1)

            x = radius1 * sin_theta1 * cos_phi1
            y = radius2 * sin_theta1 * sin_phi1
            z = radius3 * cos_theta1

            vertices.append([x, y, z])

            if i < num_segments and j < num_segments:
                first = (i * (num_segments + 1)) + j
                second = first + num_segments + 1
                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


# ------------ Mesh ------------


def gen_points(smoothness):
    step = 5.0 / smoothness
    points = []
    x = 5.0
    y = 5.0
    for i in range(smoothness * 2 + 1):
        for t in range(smoothness * 2 + 1):
            points.append([x, 0, y])
            y -= step
        y = 5.0
        x -= step
    return points


def mesh(smoothness, xvar=1.0, yvar=1.0, const=0.0):
    vertices, indices, color = [], [], []
    x, y = symbols("x y")
    # expr = xvar*cos(x) + yvar*sin(y) + const
    expr = (1 - x**2 - y**2)*exp(-1/2 * (x**2 + y**2))

    points = gen_points(smoothness)

    for point in points:
        z = expr.subs([(x, point[0]), (y, point[2])])
        point[1] = z
        vertices.append(point)
    vertices.reverse()

    counter = 0
    for i in range(len(vertices) - (2*smoothness + 1)):
        if counter == 2*smoothness:
            counter = 0
            continue
        indices.append(i)
        indices.append(i + 2*smoothness + 1)
        indices.append(i + 2*smoothness + 2)

        indices.append(i)
        indices.append(i + 2*smoothness + 2)
        indices.append(i + 1)
        counter = counter + 1

    for i in range(len(vertices)):
        color.append([1, 0, 1])
    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32), np.array(color, dtype=np.float32)


# ------------ Capture Screen ------------


def capture(save_path):
    viewport = glGetIntegerv(GL_VIEWPORT)

    pixels = glReadPixels(
        viewport[0], viewport[1], viewport[2], viewport[3], GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes(mode="RGBA", size=(
        viewport[2], viewport[3]), data=pixels)

    image = image.transpose(Image.FLIP_TOP_BOTTOM)

    image.save(save_path)
