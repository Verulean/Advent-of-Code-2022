from z3 import Solver, Real


def parse(line):
    a, b = line.split(": ")
    if b.isnumeric():
        return a, int(b)
    elif "+" in b:
        return a, b.split(" + "), "+"
    elif "-" in b:
        return a, b.split(" - "), "-"
    elif "*" in b:
        return a, b.split(" * "), "*"
    elif "/" in b:
        return a, b.split(" / "), "/"


def solve(data):
    monkeys = {}
    VARS = {}
    for line in data:
        a, *b = parse(line)
        if len(b) == 1:
            monkeys[a] = b[0]
        else:
            monkeys[a] = b

    for m in monkeys:
        VARS[m] = Real(m)

    S = Solver()
    for m, b in monkeys.items():
        if m == "humn":
            continue
        if isinstance(b, int):
            S.add(VARS[m] == b)
        else:
            (m1, m2), o = b
            if m == "root":
                S.add(VARS[m] == VARS[m1] - VARS[m2])
            elif o == "+":
                S.add(VARS[m] == VARS[m1] + VARS[m2])
            elif o == "-":
                S.add(VARS[m] == VARS[m1] - VARS[m2])
            elif o == "*":
                S.add(VARS[m] == VARS[m1] * VARS[m2])
            elif o == "/":
                S.add(VARS[m] == VARS[m1] / VARS[m2])
    S.add(VARS["root"] == 0)
    S.check()
    ans = S.model()
    return ans.eval(VARS["humn"])
