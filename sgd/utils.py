from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import datetime


def normals_triangle_strips(vertices, indices):
    face_normals = dict([(i, []) for i in range(len(vertices))])

    for i in range(len(indices) - 2):
        i_A = indices[i]
        i_B = indices[i + 1]
        i_C = indices[i + 2]

        A = vertices[i_A]
        B = vertices[i_B]
        C = vertices[i_C]

        if i % 2 == 1:
            face_normal = normal_of_face(A, B, C)
        else:
            face_normal = normal_of_face(A, C, B)

        face_normals[i_A] += [face_normal]
        face_normals[i_B] += [face_normal]
        face_normals[i_C] += [face_normal]

    return [averaged(face_normals[i]) for i in range(len(vertices))]


class Algorithm:
    def __init__(self, epochs=2000, learning_rate=0.15):
        self.epochs = epochs
        self.learning_rate = learning_rate

    def function(self, x, z):
        mountain = np.sin(x * np.pi / 15) * np.cos(z * np.pi / 15) * 10
        lake = -np.exp(-(x ** 2 + z ** 2) / 100) * 5
        return mountain + lake

    def d_function_dx(self, x, z):
        d_mountain_dx = (np.pi / 15) * np.cos(x * np.pi /
                                              15) * np.cos(z * np.pi / 15) * 10
        d_lake_dx = (2 * x / 100) * np.exp(-(x ** 2 + z ** 2) / 100) * 5
        return d_mountain_dx + d_lake_dx

    def d_function_dz(self, x, z):
        d_mountain_dz = -(np.pi / 15) * np.sin(x * np.pi /
                                               15) * np.sin(z * np.pi / 15) * 10
        d_lake_dz = (2 * z / 100) * np.exp(-(x ** 2 + z ** 2) / 100) * 5
        return d_mountain_dz + d_lake_dz

    def SGD(self, x, z):
        np.random.seed(datetime.datetime.now().microsecond)

        gx = np.random.random() * np.max(x) * 2 + np.min(x)
        gz = np.random.random() * np.max(z) * 2 + np.min(z)
        gy = self.function(gx, gz)

        points = [[gx, gy, gz]]

        for epoch in range(self.epochs):
            gx += -self.learning_rate * self.d_function_dx(gx, gz)
            gz += -self.learning_rate * self.d_function_dz(gx, gz)
            gy = self.function(gx, gz)
            points += [[gx, gy, gz]]

        return np.array(points, dtype=np.float32)


def length(v):
    return np.linalg.norm(np.array(v))


def normalize(v):
    v = np.array(v)
    return v / length(v) if length(v) > 0.0 else v


def normal_of_face(A, B, C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    n = -np.cross(B - A, C - A)
    return normalize(n)


def averaged(lst):
    s = np.array([0, 0, 0], dtype=np.float32)
    for v in lst:
        s += np.array(v)
    return normalize(s / len(lst))


def generate_sphere_sgd():
    radius = 0.5
    stack, sector = 32, 32
    raw_vertices, raw_colors, raw_indices = [], [], []

    stack_step = np.pi / stack
    sector_step = 2 * np.pi / stack

    for index1 in range(stack + 1):
        stack_angle = np.pi / 2 - index1 * stack_step
        for index2 in range(sector):
            sector_angle = -index2 * sector_step
            x = radius * np.cos(stack_angle) * np.cos(sector_angle)
            y = radius * np.sin(stack_angle)
            z = radius * np.cos(stack_angle) * np.sin(sector_angle)
            raw_vertices += [[x, y, z]]

        raw_vertices += [[radius *
                          np.cos(stack_angle), radius * np.sin(stack_angle), 0]]

    for index1 in range(stack):
        wrap_around_sector_count = sector + 1
        for index2 in range(wrap_around_sector_count):
            raw_indices += [index1 * wrap_around_sector_count + index2,
                            (index1 + 1) * wrap_around_sector_count + index2]

    raw_normals = normals_triangle_strips(
        raw_vertices, raw_indices)
    raw_colors = [0, 0.75, 0.75] * len(raw_vertices)

    return np.array(raw_vertices, dtype=np.float32), np.array(raw_normals, dtype=np.float32), np.array(raw_colors, dtype=np.float32),  np.array(raw_indices)


def generate_function_sgd(xs, zs, sgd_algorithm):
    raw_vertices = []
    raw_indices = []
    max = 0
    min = 0

    for z in zs:
        for x in xs:
            y = sgd_algorithm.function(x, z)
            max = max(max, y)
            min = min(min, y)

            raw_vertices += [[x, y, z]]

    for z_i in range(len(zs) - 1):
        if z_i % 2 == 0:
            for x_i in range(len(xs)):
                raw_indices += [z_i * len(zs) +
                                x_i, ((z_i + 1) * len(zs)) + x_i]
        else:
            for x_i in reversed(range(len(xs))):
                raw_indices += [((z_i + 1) * len(zs)) +
                                x_i, z_i * len(zs) + x_i]

    raw_normals = normals_triangle_strips(
        raw_vertices, raw_indices)
    raw_colors = []

    colormap = plt.get_cmap('plasma', 7)
    for vertex in raw_vertices:
        raw_colors += colormap((vertex[1] - min)/(max-min))[:3]

    return np.array(raw_vertices, dtype=np.float32), np.array(raw_normals, dtype=np.float32), np.array(raw_colors, dtype=np.float32), np.array(raw_indices)


class Object(ABC, object):
    @abstractmethod
    def __init__(self, shader):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def draw(self, projection, view, model):
        pass

    def key_handler(self, key):
        pass
