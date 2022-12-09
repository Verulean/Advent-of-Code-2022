import numpy as np


DIRS = {
    "U": np.array([0, 1]),
    "D": np.array([0, -1]),
    "L": np.array([-1, 0]),
    "R": np.array([1, 0]),
}


def sign(x):
    return 0 if x == 0 else -1 if x < 0 else 1


def trail(head, tail):
    di, dj = head - tail
    if di == dj == 0:
        return False
    if abs(di) > 1 or abs(dj) > 1:
        tail[0] += sign(di)
        tail[1] += sign(dj)
    return True


def solve(data):
    knots = [np.zeros(2, dtype=int) for _ in range(10)]
    v1 = {(0, 0)}
    v2 = {(0, 0)}
    for line in data:
        d, l = line.split()
        offset = DIRS[d]
        for _ in range(int(l)):
            knots[0] += offset
            for i in range(9):
                if not trail(knots[i], knots[i + 1]):
                    break
            v1.add(tuple(knots[1]))
            v2.add(tuple(knots[-1]))
    return len(v1), len(v2)
