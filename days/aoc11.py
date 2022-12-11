from collections import deque
from copy import deepcopy
from util import ints


fmt_dict = {"sep": "\n\n"}


def parse_monkeys(data):
    monkeys = []
    items = []
    for monkey in data:
        lines = monkey.split("\n")
        monkeys.append(
            (
                eval(f"lambda old: {lines[2].split(' = ')[1]}"),
                *(ints(l)[0] for l in lines[3:]),
            )
        )
        items.append(deque(ints(lines[1])))
    return monkeys, items


def run(monkeys, monkey_items, rounds, manage_worry):
    inspections = [0] * len(monkeys)
    for _ in range(rounds):
        for i, (monkey, items) in enumerate(zip(monkeys, monkey_items)):
            func, d, t, f = monkey
            inspections[i] += len(items)
            for worry in items:
                worry = manage_worry(func(worry))
                monkey_items[t if worry % d == 0 else f].append(worry)
            items.clear()
    inspections.sort(reverse=True)
    return inspections[0] * inspections[1]


def solve(data):
    monkeys, items1 = parse_monkeys(data)
    items2 = deepcopy(items1)
    D = 1
    for monkey in monkeys:
        D *= monkey[1]
    return (
        run(monkeys, items1, 20, lambda x: x // 3),
        run(monkeys, items2, 10_000, lambda x: x % D),
    )
