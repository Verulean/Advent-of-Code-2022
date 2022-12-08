from util import lmap
import numpy as np


def scan(vec, visible, scenic_scores):
    indices = [-1] * 10
    for i, elem in enumerate(vec):
        j = max(indices[elem:])
        if j < 0:
            visible[i] = 1
            scenic_scores[i] *= i
        else:
            scenic_scores[i] *= i - j
        indices[elem] = i


def solve(data):
    grid = np.array([lmap(int, row) for row in data], dtype=int)
    m, n = grid.shape

    visible = np.zeros_like(grid)
    scores = np.ones_like(grid)

    for i in range(m):
        scan(grid[i], visible[i], scores[i])
        scan(grid[i, ::-1], visible[i, ::-1], scores[i, ::-1])
    for j in range(n):
        scan(grid[:, j], visible[:, j], scores[:, j])
        scan(grid[::-1, j], visible[::-1, j], scores[::-1, j])
    return visible.sum(), scores.max()
