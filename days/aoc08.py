from util import lmap
import numpy as np


def scan(vec, visible, viewing_distance):
    indices = [-1] * 10
    for i, elem in enumerate(vec):
        j = max(indices[elem:])
        if j < 0:
            visible[i] = 1
            viewing_distance[i] *= i
        else:
            viewing_distance[i] *= i - j
        indices[elem] = i


def solve(data):
    grid = np.array([lmap(int, row) for row in data], dtype=int)
    m, n = grid.shape

    V = np.zeros_like(grid)
    S = np.ones_like(grid)

    for i in range(m):
        scan(grid[i], V[i], S[i])
        scan(grid[i, ::-1], V[i, ::-1], S[i, ::-1])
    for j in range(n):
        scan(grid[:, j], V[:, j], S[:, j])
        scan(grid[::-1, j], V[::-1, j], S[::-1, j])
    return V.sum(), S.max()
