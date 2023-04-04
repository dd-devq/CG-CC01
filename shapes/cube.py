# ------------ Package Import ------------
import glfw
import numpy as np

# ------------ Library Import ------------
from libs.buffer import *
from libs import transform as T
from libs.shader import *
from libs.utils import *


class Cube(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices = np.array(
            [
                [-1.0, -1.0, +1.0],  # 0
                [+1.0, -1.0, +1.0],  # 1
                [+1.0, +1.0, +1.0],  # 2
                [-1.0, +1.0, +1.0],  # 3
                [-1.0, -1.0, -1.0],  # 4
                [+1.0, -1.0, -1.0],  # 5
                [+1.0, +1.0, -1.0],  # 6
                [-1.0, +1.0, -1.0]   # 7
            ], dtype=np.float32
        )

        self.indices = np.array(
            [
                7, 6, 4, 5, 1, 6, 2, 7, 3, 4, 0, 1, 3, 2
            ], dtype=np.uint32
        )

        self.normals = calculate_vertex_normals_2(self.vertices, self.indices)

        self.colors = np.array(
            [
                [1, 0, 0],  # 0
                [1, 0, 1],  # 1
                [1, 1, 1],  # 2
                [1, 1, 0],  # 3
                [0, 0, 0],  # 4
                [0, 0, 1],  # 5
                [0, 1, 1],  # 6
                [0, 1, 0]   # 7
            ], dtype=np.float32
        )

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
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
        elif key == glfw.KEY_3:
            capture("result/cube/cube-gouraud.png")
        elif key == glfw.KEY_4:
            capture("result/cube/cube-gouraud-wireframe.png")


class CubePhong(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices = np.array(
            [
                [-1.0, -1.0, +1.0],  # 0
                [+1.0, -1.0, +1.0],  # 1
                [+1.0, +1.0, +1.0],  # 2
                [-1.0, +1.0, +1.0],  # 3
                [-1.0, -1.0, -1.0],  # 4
                [+1.0, -1.0, -1.0],  # 5
                [+1.0, +1.0, -1.0],  # 6
                [-1.0, +1.0, -1.0]   # 7
            ], dtype=np.float32
        )

        self.indices = np.array(
            [
                7, 6, 4, 5, 1, 6, 2, 7, 3, 4, 0, 1, 3, 2
            ], dtype=np.uint32
        )

        self.normals = calculate_vertex_normals_2(self.vertices, self.indices)

        self.colors = np.array(
            [
                [1, 0, 0],  # 0
                [1, 0, 1],  # 1
                [1, 1, 1],  # 2
                [1, 1, 0],  # 3
                [0, 0, 0],  # 4
                [0, 0, 1],  # 5
                [0, 1, 1],  # 6
                [0, 1, 0]   # 7
            ], dtype=np.float32
        )

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)

    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3, dtype=GL.GL_FLOAT)
        self.vao.add_vbo(1, self.colors, ncomponents=3, dtype=GL.GL_FLOAT)
        self.vao.add_vbo(2, self.normals, ncomponents=3, dtype=GL.GL_FLOAT)
        self.vao.add_ebo(self.indices)

        normalMat = np.identity(4, dtype=np.float32)

        I_light = np.array([[0.9, 0.4, 0.6],
                            [0.9, 0.4, 0.6],
                            [0.9, 0.4, 0.6]], dtype=np.float32)
        light_pos = np.array([0, 0.5, 0.9], dtype=np.float32)
        K_materials = np.array([[0.6, 0.4, 0.7],
                                [0.6, 0.4, 0.7],
                                [0.6, 0.4, 0.7]], dtype=np.float32)
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
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
        elif key == glfw.KEY_3:
            capture("result/cube/cube-phong.png")
        elif key == glfw.KEY_4:
            capture("result/cube/cube-phong-wireframe.png")
