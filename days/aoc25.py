class SNAFU:
    __base = 5
    __digits = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
    __rev_digits = {v: k for k, v in __digits.items()}

    @staticmethod
    def snafu2dec(n: str) -> int:
        return sum(SNAFU.__digits[d] * SNAFU.__base ** p for p, d in enumerate(reversed(n)))
    
    @staticmethod
    def dec2snafu(n: int) -> str:
        ret = ""
        while n:
            ret += SNAFU.__rev_digits[(n + 2) % 5 - 2]
            n //= SNAFU.__base
        return ret[::-1]

def solve(data):
    return SNAFU.dec2snafu(sum(map(SNAFU.snafu2dec, data)))
