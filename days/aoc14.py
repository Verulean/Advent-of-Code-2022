from util import ints, lmap


def parse(x):
    return lmap(ints, x.split("->"))


class RegolithReservoir:
    def __init__(self, rocks, max_y, source, floor=False):
        self.__rocks = rocks
        self.__max_y = max_y
        self.__source = source
        self.__tiles = self.__rocks.copy()
        self.floor = floor

    def clear(self):
        self.__tiles = self.__rocks.copy()

    def __simulate_drop(self):
        if self.__source in self.__tiles:
            return False
        x, y = self.__source
        while True:
            if not self.floor:
                if y == self.__max_y:
                    break
            elif y == self.__max_y + 1:
                self.__tiles.add((x, y))
                return True
            y += 1
            if (x, y) not in self.__tiles:
                continue
            elif (x - 1, y) not in self.__tiles:
                x -= 1
                continue
            elif (x + 1, y) not in self.__tiles:
                x += 1
                continue
            else:
                self.__tiles.add((x, y - 1))
                return True

    def dump_sand(self):
        while self.__simulate_drop():
            pass
        return len(self.__tiles) - len(self.__rocks)


def solve(data):
    data = lmap(parse, data)
    rocks = set()
    max_y = 0
    for line in data:
        for (x1, y1), (x2, y2) in zip(line, line[1:]):
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            max_y = max(max_y, y2)
            rocks.update(
                (x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)
            )
    r = RegolithReservoir(rocks, max_y, (500, 0))
    ans1 = r.dump_sand()
    r.clear()
    r.floor = True
    ans2 = r.dump_sand()
    return ans1, ans2
