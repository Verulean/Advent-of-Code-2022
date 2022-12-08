from util import lmap
import numpy as np


def is_visible(grid, i, j):
    v = grid[i, j]
    m, n = grid.shape
    if i in {0, m - 1} or j in {0, n - 1}:
        return True
    if max(grid[0:i, j]) < v:
        return True
    if max(grid[i + 1 : m, j]) < v:
        return True
    if max(grid[i, 0:j]) < v:
        return True
    if max(grid[i, j + 1 : n]) < v:
        return True
    return False


def score(grid, i, j):
    v = grid[i, j]
    m, n = grid.shape
    s1 = 0
    for I in range(i - 1, -1, -1):
        s1 += 1
        if grid[I, j] >= v:
            break
    s2 = 0
    for I in range(i + 1, m, 1):
        s2 += 1
        if grid[I, j] >= v:
            break
    s3 = 0
    for J in range(j - 1, -1, -1):
        s3 += 1
        if grid[i, J] >= v:
            break
    s4 = 0
    for J in range(j + 1, n, 1):
        s4 += 1
        if grid[i, J] >= v:
            break
    return s1 * s2 * s3 * s4


def solve(data):
    grid = np.array([lmap(int, row) for row in data], dtype=int)

    N = 0
    S = 0
    m, n = grid.shape
    for i in range(m):
        for j in range(n):
            if is_visible(grid, i, j):
                N += 1
            S = max(S, score(grid, i, j))

    return N, S
