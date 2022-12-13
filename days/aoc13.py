from util import chunks


def f(a, b):
    if isinstance(a, list) and isinstance(b, list):
        la = len(a)  # 1
        lb = len(b)  # 1
        n = min(la, lb)
        for i in range(n):
            x = f(a[i], b[i])
            if isinstance(x, bool):
                return x
        if la < lb:
            return True
        elif lb < la:
            return False
        return None
    elif isinstance(a, int) and isinstance(b, int):
        if a < b:
            return True
        elif a > b:
            return False
        return None
    elif isinstance(b, list):
        return f([a], b)
    return f(a, [b])


def solve(data):
    ans1 = 0
    i = 1
    data = [eval(line) for line in data if line.strip()]

    for a, b in chunks(data, 2):
        if f(a, b):
            ans1 += i
        i += 1

    data.extend([[[2]], [[6]]])
    sorted_data = []
    while data:
        for i, elem in enumerate(data):
            if all(f(elem, other) for other in data if other != elem):
                del data[i]
                sorted_data.append(elem)
                break
    ans2 = (sorted_data.index([[2]]) + 1) * (sorted_data.index([[6]]) + 1)

    return ans1, ans2
