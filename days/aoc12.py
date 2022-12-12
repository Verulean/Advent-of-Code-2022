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


def dijkstra(
    grid,
    start,
    end_condition,
    adj_filter=lambda grid, node, adj: False,
    cost_func=lambda grid, node, adj, cost: cost + 1,
):
    if getattr(end_condition, "__call__", None) is None:
        END = end_condition
        end_condition = lambda grid, node: node == END
    m, n = grid.shape
    q = PriorityQueue()
    q.push((0, start))
    g = np.full_like(grid, np.iinfo(grid.dtype).max)
    g[start] = 0
    while q:
        cost, node = q.pop()
        if end_condition(grid, node):
            return g[node]
        for adj in neighbors(*node):
            if not (0 <= adj[0] < m and 0 <= adj[1] < n) or adj_filter(
                grid, node, adj
            ):
                continue
            new_cost = cost_func(grid, node, adj, cost)
            if new_cost < g[adj]:
                g[adj] = new_cost
                q.push((new_cost, adj))


def solve(data):
    grid = np.array(lmap(list, data))
    S = tuple(np.argwhere(grid == "S")[0])
    E = tuple(np.argwhere(grid == "E")[0])
    grid[S] = "a"
    grid[E] = "z"
    grid = np.vectorize(ordch)(grid)
    return (
        dijkstra(grid, S, E, lambda g, n, a: g[a] - g[n] > 1),
        dijkstra(
            grid, E, lambda g, n: g[n] == 0, lambda g, n, a: g[n] - g[a] > 1
        ),
    )
