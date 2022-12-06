fmt_dict = {"sep": None}


def solve(data):
    n = 14
    for i in range(len(data) - n):
        if len(set(data[i:i+n])) == n:
            return i + n
