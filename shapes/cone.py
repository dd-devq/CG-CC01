from libs.buffer import *
from libs import transform as T
from libs.shader import *
from libs.utils import *
import ctypes
import glfw
import math
import numpy as np


def create_cone(num_segments, height, radius):
    vertices, indices, color = [], [], []
    angle_step = 2.0 * np.pi / num_segments

    vertices.append([0.0, height, 0.0])
    color.append([1, 0, 1])

    for i in range(num_segments):
        angle = i * angle_step
        x = radius * np.cos(angle)
        y = -height
        z = radius * np.sin(angle)
        vertices.append([x, y, z])
        color.append([1, 0, 1])
    color.append([1, 0, 1])

    for i in range(num_segments - 1):
        indices.append(i + 1)
        indices.append(0)
        indices.append(i + 2)

    indices.append(num_segments)
    indices.append(0)
    indices.append(1)
    vertices.append([0.0, -height, 0.0])

    for i in range(1, len(vertices) - 1):
        indices.append(i)
        indices.append(len(vertices) - 1)

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    color = np.array(color, dtype=np.float32)
    return vertices, indices, color


class Cone(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices, self.colors = create_cone(32, 2.0, 1.5)

        # self.normals = generate_normals(self.vertices, self.indices)
        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)

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
        GL.glDrawElements(GL.GL_TRIANGLES,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
