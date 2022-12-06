from util import ints
import numpy as np


def solve(data):
    l1, h1, l2, h2 = np.array([ints(line, False) for line in data]).T
    return (
        np.count_nonzero(((l1 <= l2) & (h2 <= h1)) | ((l2 <= l1) & (h1 <= h2))),
        np.count_nonzero(~((h1 < l2) | (h2 < l1))),
    )
