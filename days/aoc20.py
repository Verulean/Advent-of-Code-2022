fmt_dict = {"cast_type": int}


def score(right, ZERO):
    ret = 0
    node = ZERO
    for _ in range(3):
        for j in range(1000):
            node = right[node]
        ret += node[1]
    return ret


def mix(left, right, order, N):
    for node in order:
        i, v = node
        if v == 0:
            continue
        l, r = left[node], right[node]
        left[r] = l
        right[l] = r
        if v > 0:
            next_node = right[node]
            for _ in range((v - 1) % (N - 1)):
                next_node = right[next_node]
            nnext_node = right[next_node]
            right[next_node] = node
            left[node] = next_node
            left[nnext_node] = node
            right[node] = nnext_node
        else:
            next_node = left[node]
            for _ in range((-v - 1) % (N - 1)):
                next_node = left[next_node]
            nnext_node = left[next_node]
            left[next_node] = node
            right[node] = next_node
            right[nnext_node] = node
            left[node] = nnext_node


def solve(data):
    decryption_key = 811589153
    N = len(data)
    data2 = [n * decryption_key for n in data]
    l1, l2, r1, r2 = {}, {}, {}, {}
    z1, z2 = None, None
    for i, (v1, v2) in enumerate(zip(data, data2)):
        l = (i - 1) % N
        r = (i + 1) % N
        l1[(i, v1)] = (l, data[l])
        r1[(i, v1)] = (r, data[r])
        l2[(i, v2)] = (l, data2[l])
        r2[(i, v2)] = (r, data2[r])
        if z1 is None and v1 == 0:
            z1 = (i, v1)
        if z2 is None and v2 == 0:
            z2 = (i, v2)

    mix(l1, r1, enumerate(data), N)
    for _ in range(10):
        mix(l2, r2, enumerate(data2), N)

    return score(r1, z1), score(r2, z2)
