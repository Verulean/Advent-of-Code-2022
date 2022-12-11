from collections import defaultdict
from util import ints


def solve(data):
    items = dict()
    ops = dict()
    divs = dict()
    insp = defaultdict(int)

    monkeys = set()

    monkey = None
    for line in data:
        if line.startswith("Monkey"):
            monkey = int(line.split()[1][:-1])
            monkeys.add(monkey)
        elif "Starting items" in line:
            items[monkey] = ints(line)
        elif "Operation:" in line:
            ops[monkey] = eval(f"lambda old: {line.split(' = ')[1]}")
        elif "Test: divisible" in line:
            n = ints(line)
            divs[monkey] = n
        elif "If true:" in line or "If false:" in line:
            divs[monkey].extend(ints(line))

    D = 1
    for x in divs.values():
        D *= x[0]

    monkeys = sorted(monkeys)
    for _ in range(10000):  # range(20): # Part 1
        for monkey in monkeys:
            if not items[monkey]:
                continue
            d, tfunc, ffunc = divs[monkey]
            while items[monkey]:
                v = items[monkey].pop(0)
                v = ops[monkey](v)
                v = v % D  # v // 3 # Part 1
                f = (tfunc, ffunc)[v % d != 0]
                items[f].append(v)
                insp[monkey] += 1
    s = sorted(insp.values(), reverse=True)
    return s[0] * s[1]
