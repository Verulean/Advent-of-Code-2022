from util import ints


fmt_dict = {"cast_type": ints}


def sensed(sensors, x, y):
    for xs, ys, d in sensors:
        if abs(x - xs) + abs(y - ys) <= d:
            return True
    return False


def invalid_positions(sensors, beacons, y=2_000_000):
    invalid = set()
    for xs, ys, d in sensors:
        dx = d - abs(y - ys)
        if dx < 0:
            continue
        invalid.update(range(xs - dx, xs + dx + 1))
    invalid.difference_update(xb for xb, yb in beacons if yb == y)
    return len(invalid)


def find_beacon(sensors, min_coord=0, max_coord=4_000_000):
    for x, y, d in sensors:
        for dy in range(d + 2):
            dx = d + 1 - dy
            candidates = {
                (x - dx, y - dy),
                (x - dx, y + dy),
                (x + dx, y - dy),
                (x + dx, y + dy),
            }
            for xx, yy in candidates:
                if not (0 <= xx <= max_coord and 0 <= yy <= max_coord):
                    continue
                if not sensed(sensors, xx, yy):
                    return xx * max_coord + yy


def solve(data):
    sensors = []
    beacons = set()
    for xs, ys, xb, yb in data:
        d = abs(xb - xs) + abs(yb - ys)
        sensors.append((xs, ys, d))
        beacons.add((xb, yb))

    return invalid_positions(sensors, beacons), find_beacon(sensors)
