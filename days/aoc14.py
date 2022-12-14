from util import ints, lmap


def parse(x):
    return lmap(ints, x.split("->"))


def dump_sand(source, walls, max_y, floor=False):
    si, sj = source
    reservoir = {source}

    i, j = source
    moving = True
    while True:
        if moving:
            if not floor:
                if j == max_y:
                    reservoir.discard((i, j))
                    break
            elif j == max_y:
                moving = False

            j += 1
            if (i, j) not in reservoir and (i, j) not in walls:
                reservoir.discard((i, j - 1))
                reservoir.add((i, j))
            elif (i - 1, j) not in reservoir and (
                i - 1,
                j,
            ) not in walls:
                reservoir.discard((i, j - 1))
                reservoir.add((i - 1, j))
                i -= 1
            elif (i + 1, j) not in reservoir and (
                i + 1,
                j,
            ) not in walls:
                reservoir.discard((i, j - 1))
                reservoir.add((i + 1, j))
                i += 1
            else:
                moving = False
        elif source in reservoir:
            break
        else:
            reservoir.add(source)
            i, j = source
            moving = True
    return len(reservoir)


def solve(data):
    data = lmap(parse, data)
    sand_source = (500, 0)

    walls = set()
    max_y = 0
    for line in data:
        for (x1, y1), (x2, y2) in zip(line, line[1:]):
            if x1 == x2:
                if y1 > y2:
                    y1, y2 = y2, y1
                max_y = max(max_y, y2)
                for y in range(y1, y2 + 1):
                    walls.add((x1, y))
            else:
                if x1 > x2:
                    x1, x2 = x2, x1
                max_y = max(max_y, y1)
                for x in range(x1, x2 + 1):
                    walls.add((x, y1))
    ans1 = dump_sand(sand_source, walls, max_y)
    ans2 = dump_sand(sand_source, walls, max_y, floor=True)
    return ans1, ans2
