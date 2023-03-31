import time

import numpy as np


# the clockwise face will be the outward face (bright face)
def normal_of_face(A, B, C):
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    AC = C - A
    AB = B - A
    n = np.cross(AC, AB)
    n = n/np.linalg.norm(n)
    return n


def normal_of_vert(adjacent_face_normals):
    n = np.sum(adjacent_face_normals, axis=0)
    if np.linalg.norm(n) == 0:  # [0, 0, 0] vector
        return [0, 0, 0]
    n = n / np.linalg.norm(n)
    return n


def generate_normals(vertices, indices):
    faces = []
    for i in range(int(len(indices)/3)):
        face_vertices = tuple([tuple(vertices[index])
                              for index in indices[i*3:(i+1)*3]])
        faces.append(face_vertices)

    face_normals = {}
    for face in faces:
        face_vertex_1, face_vertex_2, face_vertex_3 = face
        face_normals[face] = normal_of_face(
            face_vertex_1, face_vertex_2, face_vertex_3)

    vertex_normals = []
    for vertex in vertices:
        adjacent_faces = filter(lambda face: vertex in face, faces)
        adjacent_face_normals = [face_normals[face] for face in adjacent_faces]

        vertex_normals.append(normal_of_vert(adjacent_face_normals))

    return vertex_normals
