from util import lmap
import numpy as np


def scan(vec, visible, viewing_distance):
    indices = [-1] * 10
    for i, elem in enumerate(vec):
        j = max(indices[elem:])
        if j < 0:
            visible[i] = 1
            viewing_distance[i] = i
        else:
            viewing_distance[i] = i - j
        indices[elem] = i


def solve(data):
    grid = np.array([lmap(int, row) for row in data], dtype=int)
    m, n = grid.shape

    V = np.zeros_like(grid)
    L = np.zeros_like(grid)
    R = np.zeros_like(grid)
    U = np.zeros_like(grid)
    D = np.zeros_like(grid)

    for i in range(m):
        scan(grid[i], V[i], L[i])
        scan(grid[i, ::-1], V[i, ::-1], R[i, ::-1])
    for j in range(n):
        scan(grid[:, j], V[:, j], U[:, j])
        scan(grid[::-1, j], V[::-1, j], D[::-1, j])
    return V.sum(), (L * R * U * D).max()
