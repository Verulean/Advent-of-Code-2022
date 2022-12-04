def f(line, part=2):
    e1, e2 = line.split(",")
    l1, h1 = map(int, e1.split("-"))
    l2, h2 = map(int, e2.split("-"))
    
    if part == 1:
        return (l1 <= l2 and h2 <= h1) or (l2 <= l1 and h1 <= h2)
    return (l2 <= h1 <= h2) or (l1 <= h2 <= h1)
    
    
def solve(data):
    return sum(f(line, 1) for line in data), sum(map(f, data))
