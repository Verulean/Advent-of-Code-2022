from collections import deque
from util import ints


fmt_dict = {"cast_type": ints}


def sim(blueprint, simulation_time):
    _, c11, c21, c31, c32, c41, c43 = blueprint
    es = set()
    c1 = max(c11, c21, c31, c41)
    q = deque()
    q.append((simulation_time, 1, 0, 0, 0, 0, 0, 0, 0, set()))
    best = 0
    visited = {}
    while q:
        t, b1, b2, b3, b4, r1, r2, r3, r4, no = q.pop()
        if t == 0:
            best = max(best, r4)
            continue
        t -= 1
        r1 = min(r1, c1 * t - b1 * (t - 1))
        r2 = min(r2, c32 * t - b2 * (t - 1))
        r3 = min(r3, c43 * t - b3 * (t - 1))
        state = (t, b1, b2, b3, b4)
        value = r1 / c21 + r2 / c32 + r3 / c43 + r4
        if visited.get(state, -1) >= value:
            continue
        visited[state] = value
        a1 = r1 >= c11
        a2 = r1 >= c21
        a3 = r1 >= c31 and r2 >= c32
        a4 = r1 >= c41 and r3 >= c43
        s = set()
        if a1:
            s.add(1)
        if a2:
            s.add(2)
        if a3:
            s.add(3)
        if a4:
            s.add(4)
        if r1 <= c1:
            q.append(
                (t, b1, b2, b3, b4, r1 + b1, r2 + b2, r3 + b3, r4 + b4, s)
            )
        if b1 < c1 and a1 and 1 not in no:
            q.append(
                (
                    t,
                    b1 + 1,
                    b2,
                    b3,
                    b4,
                    r1 + b1 - c11,
                    r2 + b2,
                    r3 + b3,
                    r4 + b4,
                    es,
                )
            )
        if b2 < c32 and a2 and 2 not in no:
            q.append(
                (
                    t,
                    b1,
                    b2 + 1,
                    b3,
                    b4,
                    r1 + b1 - c21,
                    r2 + b2,
                    r3 + b3,
                    r4 + b4,
                    es,
                )
            )
        if b3 < c43 and a3 and 3 not in no:
            q.append(
                (
                    t,
                    b1,
                    b2,
                    b3 + 1,
                    b4,
                    r1 + b1 - c31,
                    r2 + b2 - c32,
                    r3 + b3,
                    r4 + b4,
                    es,
                )
            )
        if a4 and 4 not in no:
            q.append(
                (
                    t,
                    b1,
                    b2,
                    b3,
                    b4 + 1,
                    r1 + b1 - c41,
                    r2 + b2,
                    r3 + b3 - c43,
                    r4 + b4,
                    es,
                )
            )
    return best


def solve(data):
    ans1 = sum(sim(bp, 24) * bp[0] for bp in data)
    ans2 = 1
    for bp in data[:3]:
        ans2 *= sim(bp, 32)
    return ans1, ans2
