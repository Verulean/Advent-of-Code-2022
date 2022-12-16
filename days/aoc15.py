from util import ints


fmt_dict = {"cast_type": ints}


class Ranges:
    def __init__(self):
        self.__ranges = []

    @property
    def size(self):
        return sum(b - a + 1 for a, b in self.__ranges)

    def __prune_ranges(self):
        for i in range(len(self.__ranges) - 1):
            (x1, y1), (x2, y2) = self.__ranges[i], self.__ranges[i + 1]
            if y1 >= x2:
                del self.__ranges[i]
                self.__ranges[i] = [min(x1, x2), max(y1, y2)]
                return True
        return False

    def add(self, x, y):
        if not self.__ranges or x > self.__ranges[-1][1]:
            self.__ranges.append([x, y])
            return
        if y < self.__ranges[0][0]:
            self.__ranges.insert(0, [x, y])
            return
        overlap = False
        for i, (a, b) in enumerate(self.__ranges):
            if a <= x <= b:
                overlap = True
                self.__ranges[i][1] = max(y, b)
            if a <= y <= b:
                overlap = True
                self.__ranges[i][0] = min(x, a)
        if overlap:
            while self.__prune_ranges():
                pass
        else:
            for i, ((a, b), (c, d)) in enumerate(
                zip(self.__ranges, self.__ranges[1:])
            ):
                if b < x and y < c:
                    self.__ranges.insert(i + 1, [x, y])

    def remove(self, x):
        for i, (a, b) in enumerate(self.__ranges):
            if a <= x <= b:
                if x == a:
                    self.__ranges[i][0] = a + 1
                elif x == b:
                    self.__ranges[i][1] = b - 1
                else:
                    self.__ranges[i][1] = x - 1
                    self.__ranges.insert(i + 1, [x + 1, b])
                break


def is_hidden(sensors, x, y):
    for xs, ys, d in sensors:
        if abs(xs - x) + abs(ys - y) <= d:
            return False
    return True


def invalid_positions(sensors, beacons, y):
    r = Ranges()
    for a, b, c in sensors:
        dx = c - abs(y - b)
        if dx < 0:
            continue
        r.add(a - dx, a + dx)
    for xb, yb in beacons:
        if yb == y:
            r.remove(xb)
    return r.size


def find_beacon(sensors, lower_bound, upper_bound, score_func):
    du, dd, uu, ud, u, d = set(), set(), set(), set(), set(), set()
    for a, b, c in sensors:
        du.add(a + b + c)
        dd.add(a + b - c)
        uu.add(-a + b + c)
        ud.add(-a + b - c)
    for ydu in du:
        if ydu + 2 in dd:
            d.add(ydu + 1)
    for yuu in uu:
        if yuu + 2 in ud:
            u.add(yuu + 1)
    for yu in u:
        for yd in d:
            x, r = divmod(yd - yu, 2)
            if r:
                continue
            y = yu + x
            if (
                lower_bound <= x <= upper_bound
                and lower_bound <= y <= upper_bound
                and is_hidden(sensors, x, y)
            ):
                return score_func(x, y)
    


def solve(data):
    sensors = []
    beacons = set()
    for xs, ys, xb, yb in data:
        d = abs(xb - xs) + abs(yb - ys)
        sensors.append((xs, ys, d))
        beacons.add((xb, yb))

    return (
        invalid_positions(sensors, beacons, 2000000),
        find_beacon(sensors, 0, 4000000, lambda x, y: 4000000 * x + y),
    )
