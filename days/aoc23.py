from collections import defaultdict
from util import lmap
import numpy as np


def solve(data):
    N = 1000
    grid = np.where(np.array(lmap(list, data)) == "#", 1, 0)
    grid = np.pad(grid, N + 1)

    DIRS = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    ans2 = None
    for step in range(N):
        proposals = defaultdict(set)
        stays = set()
        for i, j in np.argwhere(grid):
            if np.count_nonzero(grid[i - 1 : i + 2, j - 1 : j + 2]) <= 1:
                stays.add((i, j))
                continue
            for di, dj in DIRS:
                if di == 0:
                    if np.count_nonzero(grid[i - 1 : i + 2, j + dj]) == 0:
                        proposals[(i + di, j + dj)].add((i, j))
                        break
                if dj == 0:
                    if np.count_nonzero(grid[i + di, j - 1 : j + 2]) == 0:
                        proposals[(i + di, j + dj)].add((i, j))
                        break
            else:
                stays.add((i, j))
        # check proposals
        next_grid = np.zeros_like(grid)
        moved = False
        for elf in stays:
            next_grid[elf] = 1
        for next_pos, elves in proposals.items():
            if len(elves) > 1:
                for elf in elves:
                    next_grid[elf] = 1
            elif len(elves) == 1:
                next_grid[next_pos] = 1
                moved = True
        if not moved and ans2 is None:
            ans2 = step + 1
            break
        grid = next_grid
        DIRS = np.roll(DIRS, -1, axis=0)
    imin = 999999999
    imax = 0
    jmin = 999999999
    jmax = 0
    for i, j in np.argwhere(grid):
        imin = min(imin, i)
        imax = max(imax, i)
        jmin = min(jmin, j)
        jmax = max(jmax, j)

    grid = grid[imin : imax + 1, jmin : jmax + 1]
    return np.count_nonzero(1 - grid), ans2
