DIRS = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}


def sign(x):
    return 0 if x == 0 else -1 if x < 0 else 1


def trail(head, tail):
    di, dj = head[0] - tail[0], head[1] - tail[1]
    if abs(di) <= 1 and abs(dj) <= 1:
        return False
    tail[0] += sign(di)
    tail[1] += sign(dj)
    return True


def solve(data):
    knots = [[0, 0] for _ in range(10)]
    v1 = {(0, 0)}
    v2 = {(0, 0)}
    for line in data:
        d, l = line.split()
        di, dj = DIRS[d]
        for _ in range(int(l)):
            knots[0][0] += di
            knots[0][1] += dj
            for i in range(9):
                if not trail(knots[i], knots[i + 1]):
                    break
            v1.add(tuple(knots[1]))
            v2.add(tuple(knots[-1]))
    return len(v1), len(v2)
