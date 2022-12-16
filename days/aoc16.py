from collections import defaultdict
from copy import deepcopy
from util import lmap


def parse(line):
    line = (
        line.replace("has flow rate=", "|")
        .replace("; tunnel leads to valves", "|")
        .replace("; tunnels lead to valves", "|")
        .replace("; tunnel leads to valve", "|")
        .replace("; tunnels lead to valve", "|")
        .replace("Valve ", "")
    )
    source, flow, other = [x.strip() for x in line.split("|")]
    others = other.split(", ")
    return source, int(flow), others


oldsorted = sorted


def sorted(x, **kwargs):
    return tuple(oldsorted(x))


def solve(data):
    data = lmap(parse, data)
    tunnels = dict()
    flows = dict()
    for s, f, o in data:
        tunnels[s] = o
        flows[s] = f

    nav_time = defaultdict(dict)
    for source, dests in tunnels.items():
        for dest in dests:
            nav_time[source][dest] = 1

    old = None
    while old != nav_time:
        old = deepcopy(nav_time)
        for source in tunnels:
            for dest in list(nav_time[source]):
                t = nav_time[source][dest]
                for dest2, t2 in nav_time[dest].items():
                    nav_time[source][dest2] = min(
                        nav_time[source].get(dest2, 9999999999), t + t2
                    )

    for s, dests in nav_time.items():
        for d in list(dests):
            if flows[d] == 0:
                del nav_time[s][d]

    WANTED = {v for v, f in flows.items() if f}

    def pressure(*seq):
        p = 0
        t = 0
        flow = 0
        curr = "AA"
        for node in seq:
            dt = nav_time[curr][node] + 1
            p += flow * dt
            flow += flows[node]
            t += dt
            curr = node
        if t < 26:
            p += flow * (26 - t)
        return p

    BEST_PRESSURES = defaultdict(lambda: defaultdict(int))
    for a in WANTED:
        ta = nav_time["AA"][a] + 1

        for b in WANTED - {a}:
            tb = nav_time[a][b] + 1
            if ta + tb > 26:
                continue
            BEST_PRESSURES[2][sorted([a, b])] = max(
                BEST_PRESSURES[2][sorted([a, b])], pressure(a, b)
            )
            for c in WANTED - {a, b}:
                tc = nav_time[b][c] + 1
                if ta + tb + tc > 26:
                    continue
                BEST_PRESSURES[3][sorted([a, b, c])] = max(
                    BEST_PRESSURES[3][sorted([a, b, c])], pressure(a, b, c)
                )
                for d in WANTED - {a, b, c}:
                    td = nav_time[c][d] + 1
                    if ta + tb + tc + td > 26:
                        continue
                    BEST_PRESSURES[4][sorted([a, b, c, d])] = max(
                        BEST_PRESSURES[4][sorted([a, b, c, d])],
                        pressure(a, b, c, d),
                    )
                    for e in WANTED - {a, b, c, d}:
                        te = nav_time[d][e] + 1
                        if ta + tb + tc + td + te > 26:
                            continue

                        BEST_PRESSURES[5][sorted([a, b, c, d, e])] = max(
                            BEST_PRESSURES[5][sorted([a, b, c, d, e])],
                            pressure(a, b, c, d, e),
                        )
                        for f in WANTED - {a, b, c, d, e}:
                            tf = nav_time[e][f] + 1
                            if ta + tb + tc + td + te + tf > 26:
                                continue

                            BEST_PRESSURES[6][
                                sorted([a, b, c, d, e, f])
                            ] = max(
                                BEST_PRESSURES[6][sorted([a, b, c, d, e, f])],
                                pressure(a, b, c, d, e, f),
                            )
                            for g in WANTED - {a, b, c, d, e, f}:
                                tg = nav_time[f][g] + 1
                                if ta + tb + tc + td + te + tf + tg > 26:
                                    continue

                                BEST_PRESSURES[7][
                                    sorted([a, b, c, d, e, f, g])
                                ] = max(
                                    BEST_PRESSURES[7][
                                        sorted([a, b, c, d, e, f, g])
                                    ],
                                    pressure(a, b, c, d, e, f, g),
                                )
                                for h in WANTED - {a, b, c, d, e, f, g}:
                                    th = nav_time[g][h] + 1
                                    if (
                                        ta + tb + tc + td + te + tf + tg + th
                                        > 26
                                    ):
                                        continue

                                    BEST_PRESSURES[8][
                                        sorted([a, b, c, d, e, f, g, h])
                                    ] = max(
                                        BEST_PRESSURES[8][
                                            sorted([a, b, c, d, e, f, g, h])
                                        ],
                                        pressure(a, b, c, d, e, f, g, h),
                                    )
                                    for i in WANTED - {a, b, c, d, e, f, g, h}:
                                        ti = nav_time[h][i] + 1
                                        if (
                                            ta
                                            + tb
                                            + tc
                                            + td
                                            + te
                                            + tf
                                            + tg
                                            + th
                                            + ti
                                            > 26
                                        ):
                                            continue
                                        BEST_PRESSURES[9][
                                            sorted([a, b, c, d, e, f, g, h, i])
                                        ] = max(
                                            BEST_PRESSURES[9][
                                                sorted(
                                                    [a, b, c, d, e, f, g, h, i]
                                                )
                                            ],
                                            pressure(
                                                a, b, c, d, e, f, g, h, i
                                            ),
                                        )

    b = 0
    for l1 in BEST_PRESSURES:
        for l2 in BEST_PRESSURES:
            for seq1, p1 in BEST_PRESSURES[l1].items():
                S1 = set(seq1)
                for seq2, p2 in BEST_PRESSURES[l2].items():
                    S2 = set(seq2)
                    if not S1 & S2 and p1 + p2 > b:
                        b = p1 + p2
    return b


# 1673, 2343
