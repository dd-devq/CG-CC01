import numpy as np


# def test():
#     radius = 0.5

#     stack_count = 16
#     sector_count = 16
#     stack_step = np.pi / stack_count
#     sector_step = 2 * np.pi / stack_count

#     raw_vertices = []
#     raw_texcoords = []
#     raw_colors = []
#     raw_indices = []

#     for stack_index in range(stack_count + 1):
#         stack_angle = np.pi / 2 - stack_index * stack_step
#         for sector_index in range(sector_count):
#             sector_angle = -sector_index * sector_step
#             x = radius * np.cos(stack_angle) * np.cos(sector_angle)
#             y = radius * np.sin(stack_angle)
#             z = radius * np.cos(stack_angle) * np.sin(sector_angle)
#             raw_vertices += [[x, y, z]]
#             raw_texcoords += [[sector_index /
#                                sector_count, stack_index / stack_count]]

#         raw_vertices += [[radius *
#                           np.cos(stack_angle), radius * np.sin(stack_angle), 0]]
#         raw_texcoords += [[1, stack_index / stack_count]]

#     for stack_index in range(stack_count):
#         wrap_around_sector_count = sector_count + 1
#         for sector_index in range(wrap_around_sector_count):
#             raw_indices += [stack_index * wrap_around_sector_count + sector_index,
#                             (stack_index + 1) * wrap_around_sector_count + sector_index]

#     # raw_normals = calculate_normals_triangle_strips(
#     #     raw_vertices, raw_indices)
#     raw_colors = [1, 1, 1] * len(raw_vertices)

#     # normals = np.array(raw_normals, dtype=np.float32)
#     texcoords = np.array(raw_texcoords, dtype=np.float32)
#     vertices = np.array(raw_vertices, dtype=np.float32)
#     colors = np.array(raw_colors, dtype=np.float32)
#     indices = np.array(raw_indices)
#     for text in vertices:
#         print(text)


# test()


def newsphere1(radius, sides):
    vertices, indices, color, texcoords = [], [], [], []
    for i in range(sides+1):
        for j in range(sides+1):
            theta = np.pi * i / sides
            phi = 2 * np.pi * j / sides
            x = radius * np.sin(theta) * np.cos(phi)
            y = radius * np.sin(theta) * np.sin(phi)
            z = radius * np.cos(theta)

            vertices += [[x, y, z]]
            color += [[0, 0, 1]]
            texcoords += [[j / sides, i / sides]]

    for j in range(sides):
        for i in range(sides):
            point = (sides+1)*j+i
            indices += [point, point+sides+1, point+1, point+sides+2]

    vertices = np.array(vertices, dtype=np.float32)
    color = np.array(color, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    texcoords = np.array(texcoords, dtype=np.float32)
    print(texcoords)
    return vertices, indices, color, texcoords


newsphere1(1, 16)
