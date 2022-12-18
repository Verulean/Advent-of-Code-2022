from util import ints


fmt_dict = {"cast_type": ints}


def solve(data):
    cubes = set(map(tuple, data))
    ans1 = 0
    xl, yl, zl, xh, yh, zh = (0,) * 6
    for i, j, k in cubes:
        xl = min(xl, i)
        xh = max(xh, i)
        yl = min(yl, j)
        yh = max(yh, j)
        zl = min(zl, k)
        zh = max(zh, k)
        for other in (
            (i + 1, j, k),
            (i - 1, j, k),
            (i, j + 1, k),
            (i, j - 1, k),
            (i, j, k + 1),
            (i, j, k - 1),
        ):
            if other not in cubes:
                ans1 += 1
    xl, yl, zl, xh, yh, zh = xl - 1, yl - 1, zl - 1, xh + 1, yh + 1, zh + 1

    ans2 = 0
    q = {(xl, yl, zl)}
    done = set()
    while q:
        e = q.pop()
        if e in done:
            continue
        i, j, k = e
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
                q.add(other)
        done.add(e)

    return ans1, ans2
