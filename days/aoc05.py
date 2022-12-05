from util import chunks, ints, lmap


fmt_dict = {"strip": False, "sep": "\n\n"}


def solve(data):
    stack = data[0].split("\n")[:-1]
    STACK = [list() for _ in range(9)]
    for line in reversed(stack):
        for i, block in enumerate(chunks(line, 4)):
            c = block[1]
            if c.isalpha():
                STACK[i].append(c)
    orders = lmap(ints, data[1].split("\n"))

    print(STACK)
    for n, source, dest in orders:
        print(f"Move {n} from {source} to {dest}")
        # PART ONE
        # for _ in range(n):
        #     try:
        #         x = STACK[source - 1].pop()
        #         STACK[dest - 1].append(x)
        #     except IndexError:
        #         pass

        # PART TWO
        x = STACK[source - 1][-n:]
        del STACK[source - 1][-n:]
        STACK[dest - 1].extend(x)
        print(STACK)

    return "".join(l[-1] if l else "" for l in STACK)
