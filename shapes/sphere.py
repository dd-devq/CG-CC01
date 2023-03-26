from libs.buffer import *
from libs import transform as T
from libs.shader import *
import ctypes
import glfw
import math
import numpy as np


def create_sphere1(radius, num_segments):
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


def create_tetrahedron():
    # define vertices of a regular tetrahedron
    vertices = [[0, 0, 1],
                [0.8165, 0, -0.5],
                [-0.4082, 0.7071, -0.5],
                [-0.4082, -0.7071, -0.5],
                ]

    # define indices of the tetrahedron's faces
    indices = [0, 1, 2,        0, 2, 3,        0, 3, 1,        1, 3, 2,]

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


def create_sphere2(num_subdivisions):
    vertices, indices = create_tetrahedron()
    for i in range(num_subdivisions):
        new_indices = []
        for j in range(0, len(indices), 3):
            face = [indices[j], indices[j+1], indices[j+2]]
            new_indices += subdivide(face, vertices)
        indices = new_indices

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


class Sphere(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices = create_sphere2(4)
        self.colors = []

        print(self.vertices)

        color = []

        for i in range(len(self.vertices)):
            color.append([1, 0, 1])

        self.colors = np.array(color, dtype=np.float32)

        self.normals = []
        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3,
                         stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3,
                         stride=0, offset=None)
        self.vao.add_ebo(self.indices)

        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)

        self.vao.activate()
        GL.glDrawElements(GL.GL_TRIANGLES,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
