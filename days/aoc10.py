from util import chunks


def solve(data):
    X = 1
    cycle = 1
    i = 0
    S = 0
    SS = ""

    def f(c, x):
        return abs((c - 1) % 40 - x)

    while i < len(data):
        if i < len(data):
            line = data[i]
            cmd, *n = line.split()
            if cmd == "noop":
                SS += [".", "#"][f(cycle, X) <= 1]
                cycle += 1
                if (cycle - 20) % 40 == 0:
                    S += cycle * X

            elif cmd == "addx":
                SS += [".", "#"][f(cycle, X) <= 1]
                cycle += 1
                if (cycle - 20) % 40 == 0:
                    S += cycle * X

                SS += [".", "#"][f(cycle, X) <= 1]
                cycle += 1
                X += int(n[0])
                if (cycle - 20) % 40 == 0:
                    S += cycle * X
        i += 1

    SS = "".join(line + "\n" for line in chunks(SS, 40))
    return S, SS
