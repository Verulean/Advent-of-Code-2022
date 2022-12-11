from collections import defaultdict, deque
from copy import deepcopy
from util import ints


fmt_dict = {"sep": "\n\n"}


def parse_monkey(m):
    lines = m.split("\n")
    monkey = [
        deque(ints(lines[1])),
        eval(f"lambda old: {lines[2].split(' = ')[1]}"),
        *[ints(l)[0] for l in lines[3:]],
    ]
    return ints(lines[0])[0], monkey


def run(monkeys, rounds, reduce):
    inspections = defaultdict(int)
    for _ in range(rounds):
        for i, monkey in monkeys.items():
            items, func, divisor, t, f = monkey
            inspections[i] += len(items)
            while items:
                worry = reduce(func(items.popleft()))
                monkeys[t if worry % divisor == 0 else f][0].append(worry)
    s = sorted(inspections.values(), reverse=True)
    return s[0] * s[1]


def solve(data):
    monkeys = {n: monkey for n, monkey in map(parse_monkey, data)}
    monkeys2 = deepcopy(monkeys)
    D = 1
    for monkey in monkeys.values():
        D *= monkey[2]
    return run(monkeys, 20, lambda x: x // 3), run(
        monkeys2, 10_000, lambda x: x % D
    )
