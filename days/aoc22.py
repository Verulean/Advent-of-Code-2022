from util import ints, words
import numpy as np


fmt_dict = {"strip": False, "sep": "\n\n"}
dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
dirs_rev = {(0, 1): "R", (0, -1): "L", (1, 0): "D", (-1, 0): "U"}


def rotate(d, direction):
    i = dirs.index(d)
    if direction == "R":
        return dirs[(i + 1) % 4]
    elif direction == "L":
        return dirs[(i - 1) % 4]
    else:
        raise ValueError


def next_pos(grid, curr_pos, direction):
    m, n = grid.shape
    next_pos = curr_pos + direction
    next_pos[0] = next_pos[0] % m
    next_pos[1] = next_pos[1] % n

    # Part 1
    # while grid[tuple(next_pos)] == 2:
    #     next_pos = next_pos + direction
    #     next_pos[0] = next_pos[0] % m
    #     next_pos[1] = next_pos[1] % n
    
    # Part 2
    if grid[tuple(next_pos)] == 2:
        i, j = curr_pos[0] % 50, curr_pos[1] % 50
        ti, tj = curr_pos[0] // 50, curr_pos[1] // 50
        D = dirs_rev[tuple(direction)]
        match (ti, tj, D):
            case (0, 1, "U"):
                n2 = [150+j, 0]
                d2 = (0, 1)#R
            case (3, 0, "L"):
                n2 = [0, 50 + i]
                d2 = (1, 0)#D
    
            case (0, 1, "L"):
                n2 = [149 - i, 0]
                d2 = (0, 1)#R
            case (2, 0, "L"):
                n2 = [49 - i, 50]
                d2 = (0, 1)#R
    
            case (1, 1, "L"):
                n2 = [100, i]
                d2 = (1, 0)#D
            case (2, 0, "U"):
                n2 = [50+j, 50]
                d2 = (0, 1)#R
    
            case (0, 2, "U"):
                n2 = [199, j]
                d2 = (-1, 0)#L
            case (3, 0, "D"):
                n2 = [0, 100 + j]
                d2 = (1, 0)#R
    
            case (0, 2, "R"):
                n2 = [149 - i, 99]
                d2 = (0, -1)#L
            case (2, 1, "R"):
                n2 = [49 - i, 149]
                d2 = (0, -1)#L
    
            case (0, 2, "D"):
                n2 = [50+j, 99]
                d2 = (0, -1)#L
            case (1, 1, "R"):
                n2 = [49, 100+i]
                d2 = (-1, 0)#U
    
            case (2, 1, "D"):
                n2 = [150 + j, 49]
                d2 = (0, -1)#L
            case (3, 0, "R"):
                n2 = [149, 50 + i]
                d2 = (-1, 0)#U
            case _:
                raise ValueError
        return np.array(n2), d2
    return next_pos, direction


def solve(data):
    field, instr = data
    nums, turns = ints(instr), words(instr)
    lines = field.split("\n")
    w = max(len(l) for l in lines)
    grid = np.zeros((len(lines), w), dtype=int)
    for i, line in enumerate(lines):
        for j, c in enumerate(line.ljust(w)):
            grid[i, j] = {" ": 2, "#": 1, ".": 0}[c]

    for i, c in enumerate(lines[0].ljust(w)):
        if c == ".":
            pos = np.array([0, i])
            break
    else:
        raise ValueError
    d = (0, 1)  # right
    for steps, turn in zip(nums, turns):
        for _ in range(steps):
            n, DD = next_pos(grid, pos, d)
            if grid[tuple(n)] == 1:
                break
            elif grid[tuple(n)] == 0:
                pos = n
                d = DD
            elif grid[tuple(n)] == 2:
                raise ValueError
        d = rotate(d, turn)
    for _ in range(nums[-1]):  # zip_longest who?
        n, DD = next_pos(grid, pos, d)
        if grid[tuple(n)] == 1:
            break
        elif grid[tuple(n)] == 0:
            pos = n
            d = DD
        elif grid[tuple(n)] == 2:
            raise ValueError
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + dirs.index(tuple(d))
