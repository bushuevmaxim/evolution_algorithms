import numpy as np


def get_matrix_from_file(lines):
    matrix = []
    for line in lines:
        row = []
        for number in line.split(' '):
            if len(number) > 0:
                row.append(int(number))
        if len(row) > 0:
            matrix.append(row)
    return matrix


def read_edges(lines):
    edges = []
    n = int(lines[0])
    for line in lines[1:]:
        row = []
        for number in line.split(' '):
            if len(number) > 0:
                row.append(int(number))
        if len(row) > 0:
            edges.append(row)
    return edges, n


def matrix_from_edges(edges, n):
    matrix = np.zeros((n, n))

    for edge in edges:
        src = edge[0]
        dest = edge[1]
        weight = edge[2]
        matrix[src - 1][dest - 1] = weight
        matrix[dest - 1][src - 1] = weight

    return matrix
