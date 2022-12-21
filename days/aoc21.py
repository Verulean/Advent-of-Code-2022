from z3 import Real, Solver
from operator import add, sub, mul, truediv

operators = {"+": add, "-": sub, "*": mul, "/": truediv}


def solve(data):
    s = Solver()
    p1_conds = []
    p2_conds = []

    for line in data:
        name, condition = line.split(": ")
        monkey = Real(name)
        match condition.split():
            case [n]:
                cond = monkey == int(n)
                if name == "humn":
                    p1_conds.append(cond)
                else:
                    s.add(cond)
            case [m1, op, m2]:
                m1, m2 = Real(m1), Real(m2)
                cond = monkey == operators[op](m1, m2)
                if name == "root":
                    p1_conds.append(cond)
                    p2_conds.append(m1 - m2 == 0)
                else:
                    s.add(cond)
            case _:
                raise ValueError(f"Unexpected input '{line}'.")

    s.push()
    for c in p1_conds:
        s.add(c)
    ans1 = s.model()[Real("root")] if s.check().r == 1 else None

    s.pop()
    for c in p2_conds:
        s.add(c)
    ans2 = s.model()[Real("humn")] if s.check().r == 1 else None

    return ans1, ans2
