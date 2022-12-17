fmt_dict = {"sep": None}


class Tetris:
    __ROCKS = (
        ((0, 1, 2, 3), (0, 0, 0, 0), (0, 1, 2, 3)),
        ((1, 0, 1, 2, 1), (0, 1, 1, 1, 2), (1, 3, 4)),
        ((0, 1, 2, 2, 2), (0, 0, 0, 1, 2), (0, 1, 4)),
        ((0, 0, 0, 0), (0, 1, 2, 3), (3,)),
        ((0, 1, 0, 1), (0, 0, 1, 1), (2, 3)),
    )

    def __init__(self, wind_pattern):
        self.__wind = tuple(1 if c == ">" else -1 for c in wind_pattern)
        self.__tiles = set()

    @staticmethod
    def __get_height(heights, cycle_start, cycle_end, index):
        if index in heights:
            return heights[index]
        cycle_length = cycle_end - cycle_start
        cycle_height = heights[cycle_end] - heights[cycle_start]
        q, r = divmod(index - cycle_start, cycle_length)
        return heights[cycle_start + r] + q * cycle_height

    def __can_move(self, xs, ys, dx=0, dy=0):
        for x, y in zip(xs, ys):
            xx, yy = x + dx, y + dy
            if not 0 <= xx < 7 or yy < 0 or (xx, yy) in self.__tiles:
                return False
        return True

    def run(self, *rock_counts):
        n_winds = len(self.__wind)
        n_rocks = len(self.__ROCKS)
        windex = 0
        max_height = -1
        peaks = [0] * 7
        heights = {}
        seen = {}
        for r in range(max(rock_counts)):
            rock_index = r % n_rocks
            xs, ys, ps = self.__ROCKS[rock_index]
            dx, dy = 2, max_height + 4
            while True:
                wind = self.__wind[windex]
                if self.__can_move(xs, ys, dx + wind, dy):
                    dx += wind
                windex = (windex + 1) % n_winds
                if self.__can_move(xs, ys, dx, dy - 1):
                    dy -= 1
                else:
                    for x, y in zip(xs, ys):
                        self.__tiles.add((x + dx, y + dy))
                    for i in ps:
                        x, y = xs[i], ys[i]
                        max_height = max(max_height, y + dy)
                        peaks[x + dx] = max(peaks[x + dx], y + dy)
                    break
            heights[r] = max_height + 1

            # Check if a cycle has been found
            k = (tuple(p - max_height for p in peaks), windex, rock_index)
            if k in seen:
                ret = tuple(
                    Tetris.__get_height(heights, seen[k], r, x - 1)
                    for x in rock_counts
                )
                return ret[0] if len(ret) == 1 else ret
            seen[k] = r
        return heights[r]


def solve(data):
    return Tetris(data).run(2022, 1_000_000_000_000)
