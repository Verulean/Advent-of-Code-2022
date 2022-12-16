from collections import defaultdict
import re

fmt_dict = {"cast_type": lambda x: re.findall(r"[A-Z]{2}|\d+", x)}


class VolcanoValves:
    def __init__(self, travel_times, flow_rates, nodes, start_node, max_time):
        self.__travel_times = travel_times
        self.__flow_rates = flow_rates
        self.__nodes = nodes
        self.__start = start_node
        self.__max_time = max_time
        self.reset()

    def reset(self, max_time=None):
        self.__best_pressures = defaultdict(lambda: defaultdict(int))
        self.__path_sets = dict()
        if max_time is not None:
            self.__max_time = max_time

    def __total_pressure(self, path):
        pressure = 0
        t = 0
        flow = 0
        curr = self.__start
        for node in path:
            dt = self.__travel_times[curr][node] + 1
            pressure += flow * dt
            flow += self.__flow_rates[node]
            t += dt
            curr = node
        pressure += flow * (self.__max_time - t)
        return pressure

    def __check_paths(self, visited, path, curr_node, curr_time=0):
        for node in self.__nodes - visited:
            t = self.__travel_times[curr_node][node] + 1
            if curr_time + t > self.__max_time:
                continue
            new_visited = visited | {node}
            n = len(new_visited)
            k = tuple(sorted(new_visited))
            new_path = path + [node]
            self.__check_paths(new_visited, new_path, node, curr_time + t)
            self.__best_pressures[n][k] = max(
                self.__best_pressures[n][k], self.__total_pressure(new_path)
            )
            self.__path_sets[k] = new_visited

    def check_paths(self):
        self.__check_paths(set(), [], self.__start)

    @property
    def best_single_pressure(self):
        return max(self.__best_pressures[max(self.__best_pressures)].values())

    @property
    def best_double_pressure(self):
        ret = 0
        for n1, s1 in self.__best_pressures.items():
            for n2, s2 in self.__best_pressures.items():
                for seq1, p1 in s1.items():
                    set1 = self.__path_sets[seq1]
                    for seq2, p2 in s2.items():
                        if not set1 & self.__path_sets[seq2]:
                            ret = max(ret, p1 + p2)
        return ret


def process_data(data):
    travel_times = defaultdict(dict)
    flow_rates = dict()
    for source, flow, *dests in data:
        for dest in dests:
            travel_times[source][dest] = 1
        flow_rates[source] = int(flow)

    changed = True
    while changed:
        changed = False
        for source, dests in travel_times.items():
            for dest, t1 in list(dests.items()):
                for dest2, t2 in travel_times[dest].items():
                    curr_time = travel_times[source].get(dest2, None)
                    new_time = t1 + t2
                    if curr_time is None or new_time < curr_time:
                        travel_times[source][dest2] = new_time
                        changed = True
    for source, dests in travel_times.items():
        travel_times[source] = {
            dest: flow
            for dest, flow in dests.items()
            if flow and dest != source
        }

    nodes = {v for v, f in flow_rates.items() if f}

    return travel_times, flow_rates, nodes


def solve(data):
    start_node = "AA"
    v = VolcanoValves(*process_data(data), start_node, 30)
    v.check_paths()
    ans1 = v.best_single_pressure
    v.reset(26)
    v.check_paths()
    ans2 = v.best_double_pressure
    return ans1, ans2
