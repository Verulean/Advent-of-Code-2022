from functools import reduce
from itertools import starmap
from operator import and_


def score(c):
    if c.islower():
        return ord(c) - ord("a") + 1
    return ord(c) - ord("A") + 27


def priority(*rucksacks):
    return sum(map(score, reduce(and_, map(set, rucksacks))))


def solve(data):
    return (
        sum(map(lambda s: priority(s[: len(s) // 2], s[len(s) // 2 :]), data)),
        sum(starmap(priority, (data[i : i + 3] for i in range(0, len(data), 3)))),
    )
