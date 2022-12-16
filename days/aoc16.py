from collections import defaultdict
import re

fmt_dict = {"cast_type": lambda x: re.findall(r"[A-Z]{2}|\d+", x)}


def total_pressure(travel_time, flow_rates, path, max_time):
    p = 0
    t = 0
    flow = 0
    curr = "AA"
    for node in path:
        dt = travel_time[curr][node] + 1
        p += flow * dt
        flow += flow_rates[node]
        t += dt
        curr = node
    if t < max_time:
        p += flow * (max_time - t)
    return p


def check_paths(
    bests,
    path_sets,
    nodes,
    travel_time,
    flow_rates,
    path,
    curr_node,
    curr_time,
    max_time,
    min_length=0,
):
    visited = set(path)
    for node in nodes - visited:
        t = travel_time[curr_node][node] + 1
        if curr_time + t > max_time:
            continue
        new_visited = visited | {node}
        n = len(new_visited)
        k = tuple(sorted(new_visited))
        new_path = path + [node]
        check_paths(
            bests,
            path_sets,
            nodes,
            travel_time,
            flow_rates,
            new_path,
            node,
            curr_time + t,
            max_time,
        )
        if n >= min_length:
            bests[n][k] = max(
                bests[n][k],
                total_pressure(travel_time, flow_rates, new_path, max_time),
            )
            path_sets[k] = new_visited


def solve(data, start_node="AA"):
    travel_time = defaultdict(dict)
    flow_rates = dict()
    for source, flow, *dests in data:
        for dest in dests:
            travel_time[source][dest] = 1
        flow_rates[source] = int(flow)

    changed = True
    while changed:
        changed = False
        for source, dests in travel_time.items():
            for dest, t1 in list(dests.items()):
                for dest2, t2 in travel_time[dest].items():
                    curr_time = travel_time[source].get(dest2, None)
                    new_time = t1 + t2
                    if curr_time is None or new_time < curr_time:
                        travel_time[source][dest2] = new_time
                        changed = True

    for source, dests in travel_time.items():
        travel_time[source] = {
            dest: flow
            for dest, flow in dests.items()
            if flow and dest != source
        }

    NODES = {v for v, f in flow_rates.items() if f}

    foo = defaultdict(lambda: defaultdict(int))
    check_paths(foo, {}, NODES, travel_time, flow_rates, [], "AA", 0, 30)
    ans1 = 0
    for seq, pressure in foo[max(foo)].items():
        ans1 = max(ans1, pressure)

    bests = defaultdict(lambda: defaultdict(int))
    path_sets = {}
    check_paths(
        bests, path_sets, NODES, travel_time, flow_rates, [], "AA", 0, 26
    )
    ans2 = 0
    for n1, s1 in bests.items():
        for n2, s2 in bests.items():
            for seq1, p1 in s1.items():
                S1 = path_sets[seq1]
                for seq2, p2 in s2.items():
                    if not S1 & path_sets[seq2]:
                        ans2 = max(ans2, p1 + p2)
    return ans1, ans2
