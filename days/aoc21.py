from z3 import Real, Solver


def solve(data):
    s = Solver()
    monkeys = {}
    conds = []
    p1_conds = []
    p2_conds = []

    def parse_condition(pieces):
        return " ".join(
            f"monkeys['{x}']" if x.isalpha() else x for x in pieces
        )

    for line in data:
        m, c = line.split(": ")
        monkeys[m] = Real(m)
        pieces = [m, "=="] + c.split()
        if m == "root":
            p1_conds.append(parse_condition(pieces))
            pieces[3] = "-"
            p2_conds.append(parse_condition(pieces))
            p2_conds.append(parse_condition([m, "==", "0"]))
        elif m == "humn":
            p1_conds.append(parse_condition(pieces))
        else:
            conds.append(parse_condition(pieces))

    for c in conds:
        s.add(eval(c))
    s.push()
    for c in p1_conds:
        s.add(eval(c))
    s.check()
    ans1 = s.model().eval(monkeys["root"])

    s.pop()
    for c in p2_conds:
        s.add(eval(c))
    s.check()
    ans2 = s.model().eval(monkeys["humn"])

    return ans1, ans2
