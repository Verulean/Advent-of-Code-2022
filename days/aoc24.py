def bound(x, N):
    return (x - 1) % (N - 2) + 1


def solve(data):
    moves = {
        "^": (-1, 0),
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
        " ": (0, 0),
    }
    M, N = len(data), len(data[0])
    w = set()
    b = {c: set() for c in ("^", ">", "v", "<")}
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            pos = (i, j)
            if c == "#":
                w.add(pos)
            elif c in b:
                b[c].add(pos)
    S = (0, data[0].index("."))
    E = (M - 1, data[-1].index("."))
    w |= {(-1, S[1]), (M, E[1])}
    t = 0
    q = {S}
    goals = [E, S, E]
    times = []
    while q:
        t += 1
        for c, arr in b.items():
            di, dj = moves[c]
            b[c] = {(bound(i + di, M), bound(j + dj, N)) for i, j in arr}
        q = (
            {(i + di, j + dj) for di, dj in moves.values() for i, j in q}
            - w
            - b["^"]
            - b["v"]
            - b[">"]
            - b["<"]
        )
        if goals[0] in q:
            q = {goals.pop(0)}
            times.append(t)
            if not goals:
                return times[0], times[-1]
