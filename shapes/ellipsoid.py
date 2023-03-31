from libs.buffer import *
from libs import transform as T
from libs.shader import *
import ctypes
import glfw
import math
import numpy as np


def create_ellipsoid(radius1, radius2, radius3, num_segments):
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


class Ellipsoid(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices = create_ellipsoid(1, 3, 1, 32)

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
