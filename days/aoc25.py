from math import ceil, log
from util import smap


class SNAFU:
    __base = 5
    __digits = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
    __rev_digits = {v: k for k, v in __digits.items()}
    __zero = __rev_digits[0]
    __min_dec = min(__rev_digits)
    __max_dec = max(__rev_digits)

    @staticmethod
    def snafu2dec(n: str) -> int:
        return sum(SNAFU.__digits[d] * SNAFU.__base ** p for p, d in enumerate(reversed(n)))
    
    @staticmethod
    def dec2snafu(n: int) -> str:
        max_pow = ceil(log(n, SNAFU.__base))
        min_vals = [0]
        max_vals = [0]
        for p in range(max_pow):
            min_vals.append(min_vals[-1] + SNAFU.__min_dec * SNAFU.__base ** p)
            max_vals.append(max_vals[-1] + SNAFU.__max_dec * SNAFU.__base ** p)
        candidates = {"": 0}
        for p in range(max_pow, -1, -1):
            mult = SNAFU.__base ** p
            new_candidates = {}
            for snafu, dec in candidates.items():
                for digit, value in SNAFU.__digits.items():
                    new_value = dec + value * mult
                    delta = n - new_value
                    if delta == 0:
                        return (snafu + digit + SNAFU.__zero * p).lstrip(SNAFU.__zero)
                    if min_vals[p] <= delta <= max_vals[p]:
                        new_candidates[snafu + digit] = new_value
            candidates = new_candidates

def solve(data):
    return SNAFU.dec2snafu(smap(SNAFU.snafu2dec, data))
