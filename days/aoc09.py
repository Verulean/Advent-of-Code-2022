import numpy as np

DIRS = {
    "U": np.array([-1, 0]),
    "D": np.array([1, 0]),
    "L": np.array([0, -1]),
    "R": np.array([0, 1]),
}


def parse_direction(line):
    direction, length = line.split()
    length = int(length)
    return DIRS[direction], length


def move_tail(h, t):
    di, dj = h - t
    if di == 0 and abs(dj) >= 2:
        t[1] += np.sign(dj)
    elif dj == 0 and abs(di) >= 2:
        t[0] += np.sign(di)
    elif not (abs(di) <= 1 and abs(dj) <= 1):
        t[0] += np.sign(di)
        t[1] += np.sign(dj)


def solve(data):
    LENGTH = 10
    visited = set()
    points = [np.array([0, 0]) for _ in range(LENGTH)]

    for line in data:
        d, l = parse_direction(line)
        for _ in range(l):
            visited.add(tuple(points[-1]))
            points[0] += d
            for i in range(LENGTH - 1):
                move_tail(points[i], points[i + 1])
    visited.add(tuple(points[-1]))
    return len(visited)
