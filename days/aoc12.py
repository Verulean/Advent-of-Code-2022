from util import lmap, ordch
import numpy as np
import heapq


def neighbors(i, j):
    return ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))


class PriorityQueue(list):
    def pop(self):
        return heapq.heappop(self)

    def push(self, value):
        return heapq.heappush(self, value)


def climb(grid, start, end, best=None):
    m, n = grid.shape
    q = PriorityQueue()
    q.push((0, start))
    g = np.full_like(grid, -1)
    g[start] = 0
    while q:
        cost, node = q.pop()
        if best is not None and cost > best:
            continue
        node = tuple(node)
        if node == end:
            return int(g[end])
        for adj in neighbors(*node):
            if not (0 <= adj[0] < m and 0 <= adj[1] < n):
                continue
            if grid[adj] - grid[node] > 1:
                continue
            if g[adj] == -1 or (cost + 1) < g[adj]:
                g[adj] = cost + 1
                q.push((cost + 1, adj))


def process(c):
    if c == "S":
        return ordch("a")
    elif c == "E":
        return ordch("z")
    return ordch(c)


def solve(data):
    grid = np.array(lmap(list, data))
    GRID = np.array([lmap(process, row) for row in data])
    S = tuple(np.argwhere(grid == "S")[0])
    E = tuple(np.argwhere(grid == "E")[0])

    a = climb(GRID, S, E)
    M = None
    for S in np.argwhere(GRID == 0):
        x = climb(GRID, tuple(S), E, M)
        if M is None:
            M = x
        elif x is not None:
            M = min(M, x)

    return a, M
