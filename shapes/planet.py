from libs.buffer import *
from libs.shader import *
from libs.utils import *
from libs import transform as T
import glfw
import numpy as np


def generate_texcoord(stk, sec, base):
    texcoords = []

    for i in range(stk + 1):
        for j in range(sec + 1):
            x = base + j / (sec * 3)
            y = i / stk
            texcoords += [[x, y]]

    texcoords = np.array(texcoords, dtype=np.float32)

    return texcoords


def surfaceNormal(A, B, C):
    AB = B - A
    AC = C - A
    res = np.cross(AB, AC)
    return res


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def generate_sphere(center, r, stk, sec):
    vertices, indices, color, triangles = [], [], [], []

    # Calculating vertex list
    stack, sector = np.meshgrid(
        np.arange(0, stk + 1, 1), np.arange(0, sec + 1, 1))

    phi = np.pi / 2 - np.pi * stack / stk
    theta = 2 * np.pi * sector / sec

    xMesh = center[0] + r * np.cos(phi) * np.cos(theta)
    yMesh = center[1] + r * np.cos(phi) * np.sin(theta)
    zMesh = center[2] + r * np.sin(phi)

    xList = xMesh.flatten(order='F')
    yList = yMesh.flatten(order='F')
    zList = zMesh.flatten(order='F')

    vertices = list(map(lambda x, y, z: [x, y, z], xList, yList, zList))

    vertices = np.array(vertices, dtype=np.float32)

    for i in range(stk):
        k1 = i * (sec + 1)
        k2 = k1 + sec + 1
        for j in range(sec):
            if i != 0:
                indices += [k1, k2, k1 + 1]
                triangles += [[k1, k2, k1 + 1]]
            if i != (stk - 1):
                indices += [k1 + 1, k2, k2 + 1]
                triangles += [[k1 + 1, k2, k2 + 1]]
            k1 += 1
            k2 += 1

    indices = np.array(indices, dtype=np.uint32)

    for i in vertices:
        color += [[0, 1, 0]]

    color = np.array(color, dtype=np.float32)

    vertexNormals = np.zeros((len(vertices), 3))

    for i in triangles:
        surfaceNormals = surfaceNormal(
            vertices[i[0]], vertices[i[1]], vertices[i[2]])
        vertexNormals[i[0]] += surfaceNormals
        vertexNormals[i[1]] += surfaceNormals
        vertexNormals[i[2]] += surfaceNormals

    vertexNormals = list(map(lambda x: normalize(x), vertexNormals))

    normals = np.array(vertexNormals, dtype=np.float32)

    return vertices, indices, color, normals


class Planet(object):
    def __init__(self, vert_shader, frag_shader, center, radius, stacks, sectors, flag):
        self.center = center
        self.radius = radius
        self.stacks = stacks
        self.sectors = sectors
        self.vertices, self.indices, self.colors, self.normals = generate_sphere(
            center, radius, stacks, sectors)

        if flag == 0:
            self.texcoords = generate_texcoord(50, 50, 0)
        elif flag == 1:
            self.texcoords = generate_texcoord(50, 50, 1/3)
        else:
            self.texcoords = generate_texcoord(50, 50, 2/3)

        self.vao = VAO()
        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)

    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3,
                         dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3,
                         dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(2, self.normals, ncomponents=3,
                         dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(3, self.texcoords, ncomponents=2,
                         dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_ebo(self.indices)

        self.uma.setup_texture(
            "texture", "resources/textures/solar_system.jpg")

        normalMat = np.identity(4, 'f')
        projection = T.ortho(-1, 1, -1, 1, -1, 1)
        modelview = np.identity(4, 'f')

        I_light = np.array([
            [0.9, 0.4, 0.6],  # diffuse
            [0.9, 0.4, 0.6],  # specular
            [0.9, 0.4, 0.6]  # ambient
        ], dtype=np.float32)
        light_pos = np.array([0, 0.5, 0.9], dtype=np.float32)

        # Materials
        K_materials = np.array([
            [0.6, 0.4, 0.7],  # diffuse
            [0.6, 0.4, 0.7],  # specular
            [0.6, 0.4, 0.7]  # ambient
        ], dtype=np.float32)

        shininess = 100.0
        mode = 1

        GL.glUseProgram(self.shader.render_idx)
        self.uma.upload_uniform_matrix4fv(normalMat, 'normalMat', True)
        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        self.uma.upload_uniform_matrix3fv(I_light, 'I_light', False)
        self.uma.upload_uniform_vector3fv(light_pos, 'light_pos')
        self.uma.upload_uniform_matrix3fv(K_materials, 'K_materials', False)
        self.uma.upload_uniform_scalar1f(shininess, 'shininess')
        self.uma.upload_uniform_scalar1i(mode, 'mode')

        return self

    def draw(self, projection, view, rotate_matrix, model):
        modelview = view @ rotate_matrix
        self.vao.activate()
        GL.glUseProgram(self.shader.render_idx)
        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):
        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
