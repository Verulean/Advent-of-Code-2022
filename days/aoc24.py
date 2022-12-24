from collections import defaultdict, deque
from util import lcm


def unit_sign(x):
    return 1 if x >= 0 else -1


class Blizzards:
    def __init__(self, blizzards, bounds):
        self.__blizzards = {0: blizzards}
        self.__bounds = bounds
        self.__cycle = lcm(
            bounds[1] - bounds[0] + 1, bounds[3] - bounds[2] + 1
        )
        for t in range(self.__cycle):
            self.__blizzards[t + 1] = self.__step(self.__blizzards[t])

    def __getitem__(self, t):
        return self.__blizzards[t % self.__cycle]

    def __bound(self, i, j):
        return (
            (i - self.__bounds[0]) % (self.__bounds[1] - self.__bounds[0] + 1)
            + self.__bounds[0],
            (j - self.__bounds[2]) % (self.__bounds[3] - self.__bounds[2] + 1)
            + self.__bounds[2],
        )

    def __step(self, blizzards):
        new_blizzards = defaultdict(set)
        for (i, j), moves in blizzards.items():
            for di, dj in moves:
                new_pos = self.__bound(i + di, j + dj)
                new_blizzards[new_pos].add((di, dj))
        return new_blizzards


class BlizzardBasin:
    def __init__(self, walls, blizzards, M, N):
        self.__walls = walls
        self.__blizzards = Blizzards(blizzards, (1, M - 2, 1, N - 2))
        self.__m = M
        self.__n = N

    def dijkstra(self, start_state, end_position):
        si, sj = start_state[:2]
        ei, ej = end_position
        di = unit_sign(ei - si)
        dj = unit_sign(ej - sj)
        q = deque([start_state])
        seen = set()
        while q:
            state = q.popleft()
            i, j, t = state
            if (
                state in seen
                or (i, j) in self.__walls
                or not (0 <= i < self.__m and 0 <= j < self.__n)
            ):
                continue
            seen.add(state)
            if (i, j) == end_position:
                return t
            for adj in (
                (i + di, j),
                (i, j + dj),
                (i - di, j),
                (i, j - dj),
                (i, j),
            ):
                if (
                    adj not in self.__blizzards[t + 1]
                    and adj not in self.__walls
                ):
                    q.append((*adj, t + 1))


def solve(data):
    directions = {
        ">": (0, 1),
        "<": (0, -1),
        "^": (-1, 0),
        "v": (1, 0),
    }
    walls = set()
    blizzards = defaultdict(set)
    M, N = len(data), len(data[0])
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            pos = (i, j)
            if c == "#":
                walls.add(pos)
            elif (d := directions.get(c, None)) is not None:
                blizzards[pos].add(d)
    b = BlizzardBasin(walls, blizzards, M, N)

    S = (0, data[0].index("."))
    E = (M - 1, data[M - 1].index("."))
    ans1 = b.dijkstra((*S, 0), E)
    ans2 = b.dijkstra((*S, b.dijkstra((*E, ans1), S)), E)
    return ans1, ans2
