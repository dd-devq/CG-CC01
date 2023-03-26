from libs.buffer import *
from libs import transform as T
from libs.shader import *
import ctypes
import glfw
import math
import numpy as np


def generate_sphere_vertices(radius, slices, stacks):
    # Generate angles

    theta = np.linspace(0, 2 * np.pi, slices)
    phi = np.linspace(0, np.pi, stacks)
    theta, phi = np.meshgrid(theta, phi)

    # Generate x, y, z coordinates
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    # Reshape the coordinates into a 1D array
    vertices = np.vstack((x.ravel(), y.ravel(), z.ravel())).T
    vertices = np.array(vertices, dtype=np.float32)
    print(vertices)
    return vertices


def generate_sphere_indices(slices, stacks):
    indices = []
    for i in range(stacks):
        for j in range(slices):
            # Calculate indices for the current stack and slice
            a = i * (slices + 1) + j
            b = a + slices + 1

            # Add indices to list
            indices.append(a)
            indices.append(b)
            indices.append(a + 1)

            indices.append(b)
            indices.append(b + 1)
            indices.append(a + 1)
    indices = np.array(indices, dtype=np.uint32)
    return indices


class Sphere(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices = generate_sphere_vertices(1, 5, 5)
        self.indices = generate_sphere_indices(5, 5)
        self.colors = np.array([

        ], dtype=np.float32)
        self.normals = []
        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3,
                         stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        self.vao.add_ebo(self.indices)

        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)

        self.vao.activate()
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
