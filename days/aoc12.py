from util import dijkstra, lmap, ordch
import numpy as np


def solve(data):
    grid = np.array(lmap(list, data))
    S = tuple(np.argwhere(grid == "S")[0])
    E = tuple(np.argwhere(grid == "E")[0])
    grid[S] = "a"
    grid[E] = "z"
    grid = np.vectorize(ordch)(grid)
    return (
        dijkstra(grid, S, E, lambda g, n, a: g[a] - g[n] > 1),
        dijkstra(grid, E, lambda g, n: g[n] == 0, lambda g, n, a: g[n] - g[a] > 1),
    )
