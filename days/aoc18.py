from collections import deque
from util import ints


fmt_dict = {"cast_type": ints}


def solve(data):
    cubes = set(map(tuple, data))
    ans1 = 0
    xl, yl, zl, xh, yh, zh = (0,) * 6
    for a, b, c in cubes:
        xl = min(xl, a)
        xh = max(xh, a)
        yl = min(yl, b)
        yh = max(yh, b)
        zl = min(zl, c)
        zh = max(zh, c)
        for other in (
            (a + 1, b, c),
            (a - 1, b, c),
            (a, b + 1, c),
            (a, b - 1, c),
            (a, b, c + 1),
            (a, b, c - 1),
        ):
            if other not in cubes:
                ans1 += 1
    xl, yl, zl, xh, yh, zh = xl - 1, yl - 1, zl - 1, xh + 1, yh + 1, zh + 1

    ans2 = 0
    q = deque([(xl, yl, zl)])
    done = set()
    while q:
        i, j, k = q.pop()
        if (i, j, k) in done:
            continue
        for other in (
            (i + 1, j, k),
            (i - 1, j, k),
            (i, j + 1, k),
            (i, j - 1, k),
            (i, j, k + 1),
            (i, j, k - 1),
        ):
            if not (xl <= i <= xh and yl <= j <= yh and zl <= k <= zh):
                continue
            elif other in cubes:
                ans2 += 1
            else:
                q.append(other)
        done.add((i, j, k))

    return ans1, ans2
