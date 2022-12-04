import numpy as np


def solve(data):
    rps_map = {"A": -1, "B": 0, "C": 1, "X": 0, "Y": 1, "Z": 2}
    a, b = np.array([[rps_map[v] for v in line.split()] for line in data]).T
    return ((b - a) % 3 * 3 + b + 1).sum(), (3 * b + (a + b) % 3 + 1).sum()
