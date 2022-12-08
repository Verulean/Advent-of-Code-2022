from util import lmap
import numpy as np


class TreeGrid:
    def __init__(self, grid):
        self.__grid = np.array(grid)
        m, n = self.__grid.shape
        self.__m = m - 1
        self.__n = n - 1

    @staticmethod
    def __scan(vec, index, max_index):
        value = vec[index]
        l = max(0, index - 1)
        r = min(max_index, index + 1)
        visible = 0
        while True:
            if vec[l] >= value:
                break
            if l == 0:
                visible = True
                break
            l -= 1
        while True:
            if vec[r] >= value:
                break
            if r == max_index:
                visible = True
                break
            r += 1
        return index - l, r - index, visible

    def __process_tree(self, i, j):
        l, r, v1 = TreeGrid.__scan(self.__grid[i], j, self.__n)
        u, d, v2 = TreeGrid.__scan(self.__grid[:, j], i, self.__m)
        return v1 | v2, l * r * u * d

    def solve(self):
        ans1 = 2 * (self.__m + self.__n)
        ans2 = 0
        for i in range(1, self.__m):
            for j in range(1, self.__n):
                visible, score = self.__process_tree(i, j)
                ans1 += visible
                ans2 = max(ans2, score)
        return ans1, ans2


def solve(data):
    return TreeGrid([lmap(int, row) for row in data]).solve()
