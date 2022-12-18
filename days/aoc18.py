from util import ints
import numpy as np


fmt_dict = {"cast_type": ints}


def solve(data):
    cubes = set(map(tuple, data))

    # part 1
    S = 0
    cuboid = np.zeros((20, 20, 20), dtype=int)
    for a, b, c in cubes:
        cuboid[a, b, c] = 1
        for other in [
            (a + 1, b, c),
            (a - 1, b, c),
            (a, b + 1, c),
            (a, b - 1, c),
            (a, b, c + 1),
            (a, b, c - 1),
        ]:
            if other not in cubes:
                S += 1
    cuboid = np.pad(cuboid, 1)

    # flood fill outside of cuboid
    seed = (0, 0, 0)
    s = {seed}
    done = set()
    n = 0
    while n != len(s):
        n = len(s)
        s2 = set()
        for a, b, c in s:
            if (a, b, c) in done:
                continue
            for other in [
                (a + 1, b, c),
                (a - 1, b, c),
                (a, b + 1, c),
                (a, b - 1, c),
                (a, b, c + 1),
                (a, b, c - 1),
            ]:
                if (
                    other not in s
                    and all(0 <= i < 22 for i in other)
                    and cuboid[other] == 0
                ):
                    s2.add(other)
        s |= s2
        done.add((a, b, c))

    # part 2
    outer = np.zeros_like(cuboid)
    for x in s:
        outer[x] = 1
    S2 = 0
    for e in np.argwhere(outer):
        a, b, c = e
        for other in [
            (a + 1, b, c),
            (a - 1, b, c),
            (a, b + 1, c),
            (a, b - 1, c),
            (a, b, c + 1),
            (a, b, c - 1),
        ]:
            if all(0 <= i < 22 for i in other) and outer[other] == 0:
                S2 += 1
    return S, S2
