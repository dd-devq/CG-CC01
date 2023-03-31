import ctypes
import glfw
import math
import numpy as np
from sympy import *

from libs.shader import *
from libs import transform as T
from libs.buffer import *
from libs.utils import *


def gen_points(smoothness):
    step = 10.0 / smoothness
    points = []
    x = 10.0
    y = 10.0
    for i in range(smoothness * 2 + 1):
        for t in range(smoothness * 2 + 1):
            points.append([x, 0, y])
            y -= step
        y = 10.0
        x -= step
    return points


def mesh(smoothness, xvar=1.0, yvar=1.0, const=0.0):
    vertices, indices, color = [], [], []
    x, y = symbols("x y")
    expr = xvar*cos(x) + yvar*sin(y) + const

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


class Mesh(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices, self.colors = mesh(20, 1, 1)
        print(len(self.vertices))
        print(self.vertices)
        print(self.indices)
        self.normals = []  # YOUR CODE HERE to compute vertex's normal using the coordinates
        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    """
    Create object -> call setup -> call draw
    """

    def setup(self):
        # setup VAO for drawing cylinder's side
        self.vao.add_vbo(0, self.vertices, ncomponents=3,
                         stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)
        # setup EBO for drawing cylinder's side, bottom and top
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


class MeshPhong(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices, self.colors = mesh(20, 1, 1)
        self.normals = generate_normals(self.vertices, self.indices)
        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    """
    Create object -> call setup -> call draw
    """

    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3,
                         dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3,
                         dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(2, self.normals, ncomponents=3,
                         dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)

        self.vao.add_ebo(self.indices)

        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        # Light
        I_light = np.array([
            [0.9, 0.4, 0.6],  # diffuse
            [0.9, 0.4, 0.6],  # specular
            [0.9, 0.4, 0.6]  # ambient
        ], dtype=np.float32)
        light_pos = np.array([0, 0.5, 0.9], dtype=np.float32)

        self.uma.upload_uniform_matrix3fv(I_light, 'I_light', False)
        self.uma.upload_uniform_vector3fv(light_pos, 'light_pos')

        # Materials
        K_materials = np.array([
            [0.6, 0.4, 0.7],  # diffuse
            [0.6, 0.4, 0.7],  # specular
            [0.6, 0.4, 0.7]  # ambient
        ], dtype=np.float32)

        self.uma.upload_uniform_matrix3fv(K_materials, 'K_materials', False)

        shininess = 100.0
        mode = 1

        self.uma.upload_uniform_scalar1f(shininess, 'shininess')
        self.uma.upload_uniform_scalar1i(mode, 'mode')

        return self

    def draw(self, projection, view, model):

        self.vao.activate()
        GL.glDrawElements(GL.GL_TRIANGLES,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
