import numpy as np
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def get_rgb_field(n: int, apples: list[tuple[int, int]], path: list[tuple[int, int]] = []):
    field: np.ndarray = np.zeros((n, n, 3))
    for i in range(n):
        for j in range(n):
            if (i, j) in apples and (i, j) in path:
                field[i][j][:] = [115, 75, 35]
            elif (i, j) in apples:
                field[i][j] = [195, 64,64]
            elif (i, j) in path:
                field[i][j] = [95, 35, 35]
            else:
                field[i][j] = [31, 137, 63]

    return field.astype(np.uint8)



def get_field(n: int, apples: list[tuple[int, int]], path: list[tuple[int, int]] = [])-> np.ndarray:
    field: np.ndarray = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if (i, j) in apples and (i, j) in path:
                field[i][j] = 0
            elif (i, j) in apples:
                field[i][j] = 2
            elif (i, j) in path:
                field[i][j] = 3
            else:
                field[i][j] = 1
    return field.astype(np.uint8)

    

def show_field_rgb(field: np.ndarray)-> Figure:
    fig, ax = plt.subplots()
    ax.imshow(field)
    ax.axis('off')
    return fig

def show_field(field: np.ndarray)-> Figure:
    fig, ax = plt.subplots()
    ax.pcolormesh(field, edgecolors='k', linewidth=1, cmap="terrain_r")
    ax.set_aspect('equal')
    ax.axis('off')
    return fig

