from collections import defaultdict, deque


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
        self.__min_i = None
        self.__max_i = None
        self.__min_j = None
        self.__max_j = None
        self.__elves = elves
        for i, j in self.__elves:
            self.__update_extrema(i, j)

    def __update_extrema(self, i, j):
        if self.__min_i is None or i < self.__min_i:
            self.__min_i = i
        if self.__max_i is None or i > self.__max_i:
            self.__max_i = i
        if self.__min_j is None or j < self.__min_j:
            self.__min_j = j
        if self.__max_j is None or j > self.__max_j:
            self.__max_j = j

    def __empty_area(self):
        return (self.__max_i - self.__min_i + 1) * (
            self.__max_j - self.__min_j + 1
        ) - len(self.__elves)

    def __elf_indices(self, i, j):
        return {
            k
            for k, (di, dj) in enumerate(self.__neighbors)
            if (i + di, j + dj) in self.__elves
        }

    def step(self):
        self.__step += 1
        proposals = defaultdict(set)
        for i, j in self.__elves:
            elf_indices = self.__elf_indices(i, j)
            if not elf_indices:
                continue
            for indices, di, dj in self.__directions:
                if not indices & elf_indices:
                    proposals[(i + di, j + dj)].add((i, j))
                    break
        moved = False
        for next_pos, elves in proposals.items():
            if len(elves) == 1:
                self.__elves.add(next_pos)
                self.__elves.difference_update(elves)
                self.__update_extrema(*next_pos)
                moved = True
        self.__directions.rotate(-1)
        return moved

    def solve(self, target_step=10):
        ans1 = None
        while self.step():
            if self.__step == 10:
                ans1 = self.__empty_area()
        return ans1, self.__step


def solve(data):
    elves = set()
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "#":
                elves.add((i, j))
    return GameOfElf(elves).solve()
