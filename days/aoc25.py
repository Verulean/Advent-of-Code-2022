from math import ceil, log


def solve(data):
    max_digits = max(map(len, data)) + ceil(log(len(data), 5))
    digits = [0] * max_digits
    s2d = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
    d2s = {d: s for s, d in s2d.items()}
    for n in data:
        for i, c in enumerate(reversed(n)):
            digits[i] += s2d[c]
    for i in range(max_digits - 1):
        q, r = divmod(digits[i] + 2, 5)
        digits[i] = r - 2
        digits[i + 1] += q
    return "".join(map(d2s.get, reversed(digits))).lstrip("0")
