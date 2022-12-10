from util import chunks


def solve(data):
    cycle = 1
    x = 1
    ans1 = 0
    screen = ""
    for line in data:
        _, *n = line.split()
        i, j = divmod(cycle - 1, 40)
        screen += (".", "#")[abs(j - x) <= 1]
        cycle += 1
        if cycle % 40 == 20:
            ans1 += cycle * x
        if n:
            i, j = divmod(cycle - 1, 40)
            screen += (".", "#")[abs(j - x) <= 1]
            cycle += 1
            x += int(n[0])
            if cycle % 40 == 20:
                ans1 += cycle * x
    return ans1, "\n".join(chunks(screen, 40))
