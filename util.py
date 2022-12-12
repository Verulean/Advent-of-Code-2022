import hashlib
import heapq
import numpy as np
import re


LETTERS = set("abcdefghijklmnopqrstuvwxyz")
VOWELS = set("aeiou")
CONSONANTS = LETTERS - VOWELS


class Neighbors:
    def __init__(self, mode=0, m=None, n=None, loop=False):
        self.__loop = loop
        self.__m = m
        self.__n = n

        if mode == 0:
            self.__offsets = ((1, 0), (0, 1), (-1, 0), (0, -1))
        elif mode == 1:
            self.__offsets = (
                (1, 0),
                (1, 1),
                (0, 1),
                (-1, 1),
                (-1, 0),
                (-1, -1),
                (0, -1),
                (1, -1),
            )

    def __call__(self, i, j):
        if self.__loop:
            for di, dj in self.__offsets:
                yield ((i + di) % self.__m, (j + dj) % self.__n)
        else:
            for di, dj in self.__offsets:
                if 0 <= i + di < self.__m and 0 <= j + dj < self.__n:
                    yield (i + di, j + dj)

    def __getitem__(self, pos):
        return self(*pos)


class PriorityQueue(list):
    def pop(self):
        return heapq.heappop(self)

    def push(self, value):
        return heapq.heappush(self, value)


def lmap(func, iterable):
    return list(map(func, iterable))


def smap(func, iterable):
    return sum(map(func, iterable))


def minmap(func, iterable):
    return min(map(func, iterable))


def maxmap(func, iterable):
    return max(map(func, iterable))


def ints(s, negatives=True):
    pattern = r"\-?\d+" if negatives else r"\d+"
    return lmap(int, re.findall(pattern, s))


def try_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def split_ints(s):
    return lmap(try_int, s.split())


def floats(s, negatives=True):
    pattern = r"-?\d+(?:\.\d+)?" if negatives else r"\d+(?:\.\d+)?"
    return lmap(float, re.findall(pattern, s))


def try_float(s):
    try:
        return float(s)
    except ValueError:
        return s


def split_floats(s):
    return lmap(try_float, s.split())


def words(s):
    return re.findall(r"[A-Za-z]+", s)


def ordch(c):
    if len(c) == 1 and c.isalpha():
        if c.islower():
            return ord(c) - ord("a")
        return ord(c) - ord("A")
    return None


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def parts(l, n):
    m = len(l) // n
    for i in range(n):
        yield l[i * m : (i + 1) * m]
    if len(l) % n:
        yield l[m * n :]


def is_unique(l):
    return len(set(l)) == len(l)


def factors(n):
    return [d for d in range(1, int(n**0.5) + 1) if n % d == 0]


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b / gcd(a, b)


def md5(s):
    h = hashlib.md5()
    h.update(s)
    return h.hexdigest()


def sha256(s):
    h = hashlib.sha256()
    h.update(s)
    return h.hexdigest()


def grid_to_string(grid, func=str, sep=""):
    return "\n".join(map(lambda seq: sep.join(map(func, seq)), grid))


def dijkstra(
    grid,
    start,
    end_condition,
    adj_filter=lambda grid, node, adj: False,
    cost_func=lambda grid, node, adj, cost: cost + 1,
):
    if getattr(end_condition, "__call__", None) is None:
        END = end_condition
        end_condition = lambda grid, node: node == END
    neighbors = Neighbors(0, *grid.shape)
    q = PriorityQueue()
    q.push((0, start))
    g = np.full_like(grid, np.iinfo(grid.dtype).max)
    g[start] = 0
    while q:
        cost, node = q.pop()
        if end_condition(grid, node):
            return g[node]
        for adj in neighbors(*node):
            if adj_filter(grid, node, adj):
                continue
            new_cost = cost_func(grid, node, adj, cost)
            if new_cost < g[adj]:
                g[adj] = new_cost
                q.push((new_cost, adj))
