from viewer import Viewer
import numpy as np
import glfw
import OpenGL.GL as GL
from utils import *
from libs.buffer import *
from libs.transform import *


class SGD(Object):
    def __init__(self):
        self.sgd_algorithm = Algorithm()
        self.xs = np.arange(-12, 12, 0.2)
        self.zs = np.arange(-12, 12, 0.2)
        self.X, self.Z = np.meshgrid(self.xs, self.zs)
        self.point_vertices, self.point_normals, self.point_colors, self.point_indices = generate_sphere_sgd()
        self.function_vertices, self.function_normals, self.function_colors, self.function_indices = generate_function_sgd(
            self.xs, self.zs, self.sgd_algorithm)

        self.point_position = None

        self.point_vao = VAO()
        self.point_shader = Shader("phong.vert", "phong.frag")
        self.point_uma = UManager(self.point_shader)

        self.function_vao = VAO()
        self.function_shader = Shader("phong.vert", "phong.frag")
        self.function_uma = UManager(self.function_shader)

        self.previous_vertices = self.sgd_algorithm.SGD(self.xs, self.xs)
        self.previous_vao = VAO()
        self.previous_shader = Shader("phong.vert", "phong.frag")
        self.previous_uma = UManager(self.previous_shader)
        self.setup_points()

    def setup_points(self):
        self.raw_previous_vertices = self.sgd_algorithm.SGD(self.xs, self.zs)
        self.raw_previous_color = [1, 0, 0] * len(self.raw_previous_vertices)
        self.raw_previous_indices = len(self.raw_previous_vertices)
        self.last_frame_time = -10
        self.current_previous_index = 0

        self.previous_vertices = np.array(
            self.raw_previous_vertices, dtype=np.float32)
        self.previous_colors = np.array(
            self.raw_previous_color, dtype=np.float32)
        self.previous_indices = np.array(self.raw_previous_indices)

    def setup(self):
        I_light = np.array([
            [1, 1, 1],  # diffuse
            [1, 1, 1],  # specular
            [1, 1, 1]  # ambient
        ], dtype=np.float32)
        light_pos = np.array([0, 0.5, 0.9], dtype=np.float32)

        K_materials = np.array([
            [1, 1, 1],  # diffuse
            [1, 1, 1],  # specular
            [1, 1, 1]  # ambient
        ], dtype=np.float32)

        self.function_vao.activate()
        self.function_vao.add_vbo(
            0, self.function_vertices, ncomponents=3, stride=0, offset=None)
        self.function_vao.add_vbo(
            1, self.function_normals, ncomponents=3, stride=0, offset=None)
        self.function_vao.add_vbo(
            3, self.function_colors, ncomponents=3, stride=0, offset=None)
        self.function_vao.add_ebo(self.function_indices)

        self.function_uma.upload_uniform_matrix3fv(I_light, 'I_light', False)
        self.function_uma.upload_uniform_vector3fv(light_pos, 'light_pos')
        self.function_uma.upload_uniform_matrix3fv(
            K_materials, 'K_materials', False)
        self.function_uma.upload_uniform_scalar1f(3, 'shininess')
        self.function_uma.upload_uniform_scalar1f(0.25, 'phong_factor')

        self.point_vao.activate()
        self.point_vao.add_vbo(0, self.point_vertices,
                               ncomponents=3, stride=0, offset=None)
        self.point_vao.add_vbo(1, self.point_normals,
                               ncomponents=3, stride=0, offset=None)
        self.point_vao.add_vbo(3, self.point_colors,
                               ncomponents=3, stride=0, offset=None)
        self.point_vao.add_ebo(self.point_indices)

        self.point_uma.upload_uniform_matrix3fv(I_light, 'I_light', False)
        self.point_uma.upload_uniform_vector3fv(light_pos, 'light_pos')
        self.point_uma.upload_uniform_matrix3fv(
            K_materials, 'K_materials', False)
        self.point_uma.upload_uniform_scalar1f(3, 'shininess')
        self.point_uma.upload_uniform_scalar1f(0.5, 'phong_factor')

        return self

    def next_point(self):
        if self.current_previous_index == len(self.raw_previous_vertices):
            return self.raw_previous_vertices[-1]

        self.current_previous_index += 1
        return self.raw_previous_vertices[self.current_previous_index - 1]

    def draw(self, projection, view, model):
        if glfw.get_time() - self.last_frame_time > 0.025:
            self.last_frame_time = glfw.get_time()
            self.point_position = self.next_point()

        GL.glUseProgram(self.point_shader.render_idx)
        self.point_uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.point_uma.upload_uniform_matrix4fv(view, 'modelview', True)
        self.point_uma.upload_uniform_matrix4fv(identity() @ translate(self.point_position[0], self.point_position[1], self.point_position[2]),
                                                'model', True)
        self.point_uma.upload_uniform_vector3fv(view, 'light_pos')
        self.point_vao.activate()

        GL.glUseProgram(self.function_shader.render_idx)
        self.function_uma.upload_uniform_matrix4fv(
            projection, 'projection', True)
        self.function_uma.upload_uniform_matrix4fv(view, 'modelview', True)
        self.function_uma.upload_uniform_matrix4fv(identity(), 'model', True)
        self.function_uma.upload_uniform_vector3fv(view, 'light_pos')
        self.function_vao.activate()
        GL.glDrawElements(
            GL.GL_TRIANGLE_STRIP, self.function_indices.shape[0], GL.GL_UNSIGNED_INT, None)

        GL.glDrawElements(GL.GL_TRIANGLE_STRIP,
                          self.point_indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):
        if key == glfw.KEY_SPACE:
            self.raw_previous_vertices = self.sgd_algorithm.SGD(
                self.xs, self.zs)
            self.raw_previous_color = [
                0, 0.4, 0.75] * len(self.raw_previous_vertices)
            self.raw_previous_indices = len(self.raw_previous_vertices)
            self.last_frame_time = -20
            self.current_previous_index = 0


glfw.init()
viewer = Viewer()
model = SGD().setup()
viewer.add(model)
viewer.run()

glfw.terminate()
