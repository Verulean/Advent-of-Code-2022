from operator import add, sub, mul, truediv, floordiv


operators = {"+": add, "-": sub, "*": mul, "/": truediv, "//": floordiv}


class MonkeyMath:
    def __init__(self, data, x, y):
        self.__x = x
        self.__y = y
        self.__input = tuple(map(self.__parse_line, data))
        self.__known = {}
        self.__unknown = {}

    def __parse_line(self, line):
        monkey, condition = line.split(": ")
        return monkey, condition.split()

    def init(self, part):
        self.__known.clear()
        self.__unknown.clear()
        for m, pieces in self.__input:
            match pieces:
                case [n]:
                    if part == 2 and m == self.__x:
                        self.__known[m] = self.__x
                    else:
                        self.__known[m] = int(n)
                case [m1, op, m2]:
                    if part == 1 and op == "/":
                        op = "//"
                    elif part == 2 and m == self.__y:
                        op = "-"
                    self.__unknown[m] = (m1, op, m2)

    def simplify(self):
        changed = True
        while changed:
            changed = False
            for m, (m1, op, m2) in list(self.__unknown.items()):
                e1 = self.__known.get(m1, None)
                e2 = self.__known.get(m2, None)
                if e1 is None or e2 is None:
                    continue
                if isinstance(e1, int) and isinstance(e2, int):
                    self.__known[m] = operators[op](e1, e2)
                else:
                    self.__known[m] = f"({e1}){op}({e2})"
                del self.__unknown[m]
                changed = True
        return eval(f"lambda {self.__x}: {self.__known[self.__y]}")


def binary_search(f, l=0, h=1024):
    while l < h:
        m = (l + h) // 2
        # root encountered
        if (fl := f(l)) == 0:
            return l
        elif (fm := f(m)) == 0:
            return m
        elif (fh := f(h)) == 0:
            return h
        # restrict bounds
        elif fl * fm < 0:
            h = m
        elif fm * fh < 0:
            l = m
        # expand bounds
        else:
            span = h - l
            h += span
            l -= span
    return l


def solve(data):
    m = MonkeyMath(data, "humn", "root")
    m.init(1)
    ans1 = m.simplify()(None)
    m.init(2)
    ans2 = binary_search(m.simplify())
    return ans1, ans2
