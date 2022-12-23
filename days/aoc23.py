from collections import deque


class GameOfElf:
    __neighbors = (
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
    )

    def __init__(self, elves):
        self.__directions = deque(
            [
                ({0, 1, 2}, -1, 0),
                ({4, 5, 6}, 1, 0),
                ({6, 7, 0}, 0, -1),
                ({2, 3, 4}, 0, 1),
            ]
        )
        self.__step = 0
        self.__elves = elves

    def __empty_area(self):
        min_i = None
        max_i = None
        min_j = None
        max_j = None
        for i, j in self.__elves:
            if min_i is None or i < min_i:
                min_i = i
            if max_i is None or i > max_i:
                max_i = i
            if min_j is None or j < min_j:
                min_j = j
            if max_j is None or j > max_j:
                max_j = j
        return (max_i - min_i + 1) * (max_j - min_j + 1) - len(self.__elves)

    def __elf_indices(self, i, j):
        return {
            k
            for k, (di, dj) in enumerate(GameOfElf.__neighbors)
            if (i + di, j + dj) in self.__elves
        }

    def step(self):
        self.__step += 1
        proposals = {}
        for i, j in self.__elves:
            elf_indices = self.__elf_indices(i, j)
            if not elf_indices:
                continue
            for indices, di, dj in self.__directions:
                if not indices & elf_indices:
                    new = (i + di, j + dj)
                    if new in proposals:
                        del proposals[new]
                    else:
                        proposals[new] = (i, j)
                    break
        moved = False
        for next_pos, elf in proposals.items():
            self.__elves.add(next_pos)
            self.__elves.remove(elf)
            moved = True
        self.__directions.rotate(-1)
        return moved

    def solve(self, target_step=10):
        ans1 = None
        while self.step():
            if ans1 is None and self.__step == 10:
                ans1 = self.__empty_area()
        return ans1, self.__step


def solve(data):
    elves = {
        (i, j)
        for i, line in enumerate(data)
        for j, c in enumerate(line)
        if c == "#"
    }
    return GameOfElf(elves).solve()
