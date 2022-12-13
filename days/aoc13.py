from util import chunks


def compare(a, b):
    la, lb = isinstance(a, list), isinstance(b, list)
    if la and lb:
        for aa, bb in zip(a, b):
            if (r := compare(aa, bb)) is not None:
                return r
        return compare(len(a), len(b))
    elif la:
        return compare(a, [b])
    elif lb:
        return compare([a], b)
    else:
        return True if a < b else False if a > b else None


def merge(A, left, right, end, B, f):
    i, j = left, right
    for k in range(left, end):
        if i < right and (j >= end or compare(A[i], A[j])):
            B[k] = A[i]
            i += 1
        else:
            B[k] = A[j]
            j += 1


def merge_sort(A, f):
    n = len(A)
    B = [None] * n
    l = 1
    while l < n:
        for i in range(0, n, l * 2):
            merge(A, i, min(i + l, n), min(i + 2 * l, n), B, f)
        A[:] = B
        l *= 2
    return A


def solve(data):
    data = [eval(line) for line in data if line]
    ans1 = sum(i + 1 for i, args in enumerate(chunks(data, 2)) if compare(*args))
    data.extend([[[2]], [[6]]])
    data = merge_sort(data, compare)
    ans2 = (data.index([[2]]) + 1) * (data.index([[6]]) + 1)
    return ans1, ans2
