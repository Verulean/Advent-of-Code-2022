from util import ints, lmap
import numpy as np


def parse(x):
    return [tuple(ints(l)) for l in x.split(" -> ")]


def indices(i, j, offset=0):
    return i, j - 426 + offset


def drop(grid):
    if grid[0, 274] == 1:
        return False
    grid[0, 274] = 1
    return True


def solve(data):
    data = lmap(parse, data)
    x1, y1 = 10000, 10000
    x2, y2 = 0, 0

    for line in data:
        for x, y in line:
            x1 = min(x1, x)
            x2 = max(x2, x)
            y1 = min(y1, y)
            y2 = max(y2, y)
    print(x1, y1, x2, y2)
    SOURCE = indices(0, 500, 200)
    print(SOURCE)

    # x 494 to 503
    # y 4 to 9
    grid = np.zeros((159, 81), dtype=int)
    M, N = grid.shape
    for line in data:
        for (a, b), (c, d) in zip(line, line[1:]):
            a, c = min(a, c), max(a, c)
            b, d = min(b, d), max(b, d)
            a, b = indices(b, a)
            c, d = indices(d, c)
            grid[a : c + 1, b : d + 1] = 2

    grid = np.pad(grid, 200)
    grid = grid[200:]
    grid[M + 1, :] = 2

    M, N = grid.shape

    moving = True
    drop(grid)
    curr_pos = SOURCE
    print(SOURCE)
    while True:
        if moving:
            i, j = curr_pos
            if i + 1 >= M:
                break
            if grid[i + 1, j] == 0:
                grid[i, j] = 0
                grid[i + 1, j] = 1
                curr_pos = (i + 1, j)
            elif j - 1 < 0 or grid[i + 1, j - 1] == 0:
                if j - 1 < 0:
                    grid[curr_pos] = 0
                    break
                grid[curr_pos] = 0
                grid[i + 1, j - 1] = 1
                curr_pos = (i + 1, j - 1)
            elif j + 1 >= N or grid[i + 1, j + 1] == 0:
                if j + 1 >= N:
                    grid[curr_pos] = 0
                    break
                grid[curr_pos] = 0
                grid[i + 1, j + 1] = 1
                curr_pos = (i + 1, j + 1)
            else:
                moving = False
        else:
            if drop(grid):
                curr_pos = SOURCE
                moving = True
            else:
                break
    return np.count_nonzero(grid == 1)
