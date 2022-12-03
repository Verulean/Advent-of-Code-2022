import numpy as np


fmt_dict = {
    'cast_type': str,
    'strip': True, 
    'sep': '\n', 
    'file_prefix': ''
    }

def score(c):
    if c == c.lower():
        return ord(c) - ord("a") + 1
    return ord(c) - ord("A") + 27
def solve(data):
    s = 0
    N = len(data)
    
    for line in data:
        a, b = line[:len(line)//2], line[len(line)//2:]
        s += sum(score(c) for c in set(a) & set(b))
    
    S = 0
    for i in range(N//3):
        s1 = set(data[3*i])
        s2 = set(data[3*i+1])
        s3 = set(data[3*i+2])
        c = s1 & s2 & s3
        S += sum(score(C) for C in c)
    return s, S