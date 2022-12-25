from collections import defaultdict
from math import ceil, log


def solve(data):
    s2d = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
    d2s = {d: s for s, d in s2d.items()}
    digits = defaultdict(int)
    max_len = 0
    for n in data:
        max_len = max(max_len, len(n))
        for i, c in enumerate(reversed(n)):
            digits[i] += s2d[c]
    for i in range(max_len + ceil(log(len(data), 5)) + 1):
        q, r = divmod(digits[i] + 2, 5)
        digits[i] = r - 2
        digits[i + 1] += q
    return "".join(d2s[d] for d in reversed(digits.values())).lstrip("0")
