def solve(data):
    moves = {
        "^": (-2, -1),
        ">": (-1, 0),
        "v": (0, -1),
        "<": (-1, -2),
    }
    M, N = len(data), len(data[0])
    w = set()
    b = {c: set() for c in moves}
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            pos = (i, j)
            if c in b:
                b[c].add(pos)
            elif c == "#":
                w.add(pos)
    S = (0, data[0].index("."))
    E = (M - 1, data[-1].index("."))
    w |= {(-1, S[1]), (M, E[1])}
    q = {S}
    dests = [E, S, E]
    times = []
    m = ((-1, 0), (0, 1), (1, 0), (0, -1), (0, 0))
    t = 0
    while q:
        t += 1
        for c, arr in b.items():
            di, dj = moves[c]
            b[c] = {
                ((i + di) % (M - 2) + 1, (j + dj) % (N - 2) + 1)
                for i, j in arr
            }
        q = {(i + di, j + dj) for di, dj in m for i, j in q}
        q -= w
        for d in b.values():
            q -= d
        if dests[0] in q:
            q = {dests.pop(0)}
            times.append(t)
            if not dests:
                break
    return times[0], times[-1]
