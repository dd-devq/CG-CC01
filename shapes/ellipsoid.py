from libs.buffer import *
from libs import transform as T
from libs.shader import *
from libs.utils import *
import ctypes
import glfw
import numpy as np


class Ellipsoid(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices = ellipsoid(1, 3, 1, 32)

        color = []

        for i in range(len(self.vertices)):
            color.append([1, 0, 1])

        self.colors = np.array(color, dtype=np.float32)

        self.normals = calculate_vertex_normals(self.vertices, self.indices)
        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)

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
        elif key == glfw.KEY_3:
            capture("result/ellipsoid/ellipsoid-gouraud.png")
        elif key == glfw.KEY_4:
            capture("result/ellipsoid/ellipsoid-gouraud-wireframe.png")


class EllipsoidPhong(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices = ellipsoid(1, 3, 1, 32)

        color = []

        for i in range(len(self.vertices)):
            color.append([1, 0, 1])

        self.colors = np.array(color, dtype=np.float32)

        self.normals = calculate_vertex_normals(self.vertices, self.indices)
        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)

    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3, dtype=GL.GL_FLOAT)
        self.vao.add_vbo(1, self.colors, ncomponents=3, dtype=GL.GL_FLOAT)
        self.vao.add_vbo(2, self.normals, ncomponents=3, dtype=GL.GL_FLOAT)
        self.vao.add_ebo(self.indices)

        normalMat = np.identity(4, dtype=np.float32)

        I_light = np.array([0.9, 0.4, 0.6], dtype=np.float32)
        light_pos = np.array([0, 0.5, 0.9], dtype=np.float32)
        K_materials = np.array([0.6, 0.4, 0.7], dtype=np.float32)

        shininess = 100.0
        mode = 1

        GL.glUseProgram(self.shader.render_idx)

        self.uma.upload_uniform_matrix4fv(normalMat, 'normalMat', True)
        self.uma.upload_uniform_matrix3fv(I_light, 'I_light', False)
        self.uma.upload_uniform_vector3fv(light_pos, 'light_pos')
        self.uma.upload_uniform_matrix3fv(K_materials, 'K_materials', False)
        self.uma.upload_uniform_scalar1f(shininess, 'shininess')
        self.uma.upload_uniform_scalar1i(mode, 'mode')
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
        elif key == glfw.KEY_3:
            capture("result/ellipsoid/ellipsoid-phong.png")
        elif key == glfw.KEY_4:
            capture("result/ellipsoid/ellipsoid-phong-wireframe.png")
