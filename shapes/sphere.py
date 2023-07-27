from libs.buffer import *
from libs import transform as T
from libs.shader import *
from libs.utils import *
import ctypes
import glfw
import numpy as np


class Sphere1(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices = sphere_1(1, 32)
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
            capture("result/sphere/sphere1-gouraud.png")
        elif key == glfw.KEY_4:
            capture("result/sphere/sphere1-gouraud-wireframe.png")


class Sphere2(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices = sphere_2(5)
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
            capture("result/sphere/sphere2-gouraud.png")
        elif key == glfw.KEY_4:
            capture("result/sphere/sphere2-gouraud-wireframe.png")


class SpherePhong1(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices = sphere_1(1, 32)
        color = []
        for i in range(len(self.vertices)):
            color.append([1, 1, 1] * self.vertices[i])

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
        GL.glDrawElements(GL.GL_TRIANGLES,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
        elif key == glfw.KEY_3:
            capture("result/sphere/sphere1-phong.png")
        elif key == glfw.KEY_4:
            capture("result/sphere/sphere1-phong-wireframe.png")


class SpherePhong2(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices = sphere_2(5)
        color = []
        for i in range(len(self.vertices)):
            color.append([1, 1, 1] * self.vertices[i])

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
        GL.glDrawElements(GL.GL_TRIANGLES,
                          self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
        elif key == glfw.KEY_3:
            capture("result/sphere/sphere2-phong.png")
        elif key == glfw.KEY_4:
            capture("result/sphere/sphere2-phong-wireframe.png")


def sphere(center, r, stk, sec):   
    vertices, indices, color, triangles = [], [], [], []
    
    # Calculating vertex list
    stackMesh, sectorMesh = np.meshgrid(np.arange(0, stk + 1, 1), np.arange(0, sec + 1, 1))

    phiMesh = np.pi / 2 - np.pi * stackMesh / stk
    thetaMesh = 2 * np.pi * sectorMesh / sec 
    
    xMesh = center[0] + r * np.cos(phiMesh) * np.cos(thetaMesh)
    yMesh = center[1] + r * np.cos(phiMesh) * np.sin(thetaMesh)
    zMesh = center[2] + r * np.sin(phiMesh)
    
    xList = xMesh.flatten(order='F')
    yList = yMesh.flatten(order='F')
    zList = zMesh.flatten(order='F')
    
    vertices = list(map(lambda x, y, z: [x, y, z], xList, yList, zList))
    
    vertices = np.array(vertices, dtype=np.float32)

    # Calculating index list
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

    # Calculating vertex color
    for i in vertices:
        color += [[0, 1, 0]]
    
    color = np.array(color, dtype=np.float32)

    # Calculating vertex normals
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

    vertexNormals = np.zeros((len(vertices), 3))
    
    for i in triangles:
        surfaceNormals = surfaceNormal(vertices[i[0]], vertices[i[1]], vertices[i[2]])
        vertexNormals[i[0]] += surfaceNormals
        vertexNormals[i[1]] += surfaceNormals
        vertexNormals[i[2]] += surfaceNormals
    
    vertexNormals = list(map(lambda x : normalize(x), vertexNormals))
    
    normals = np.array(vertexNormals, dtype=np.float32)
    
    return vertices, indices, color, normals

def texcoord(stk, sec, base):
    texcoords = []
    
    for i in range(stk + 1):
        for j in range(sec + 1):
            x = base + j / (sec * 3)
            y = i / stk
            texcoords += [[x , y]]
    
    texcoords = np.array(texcoords, dtype=np.float32)
    
    return texcoords

class TextureSphere(object):
    def __init__(self, vert_shader, frag_shader, center, radius, stacks, sectors):
        self.center = center
        self.radius = radius
        self.stacks = stacks
        self.sectors = sectors
        self.vertices, self.indices, self.colors, self.normals = sphere(center, radius, stacks, sectors) # center, radius, stacks, sectors - Sphere with stacks and sectors
        
        self.texcoords = texcoord(50, 50, 0)
        
        self.vao = VAO()
        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)

        
    def setup(self):
        self.vao.add_vbo(0, self.vertices, ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(2, self.normals, ncomponents=3, dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_vbo(3, self.texcoords, ncomponents=2, dtype=GL.GL_FLOAT, normalized=False, stride=0, offset=None)
        self.vao.add_ebo(self.indices)

        self.uma.setup_texture("texture", "./resources/textures/solar_system.jpg")
        
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

    def draw(self, projection, view, model):
        modelview = view
        self.vao.activate()
        GL.glUseProgram(self.shader.render_idx)
        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)
        
    def key_handler(self, key):
        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
            
        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2

