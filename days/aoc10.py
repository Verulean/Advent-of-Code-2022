def step(state, value=0):
    cycle, x, sigsum, screen = state
    i, j = divmod(cycle - 1, 40)
    if abs(j - x) <= 1:
        screen[i][j] = "#"
    cycle += 1
    x += value
    if j == 18:
        sigsum += cycle * x
    return [cycle, x, sigsum, screen]


def solve(instructions):
    state = [1, 1, 0, [["."] * 40 for _ in range(6)]]
    for instr in instructions:
        _, *n = instr.split()
        state = step(state)
        if n:
            state = step(state, int(n[0]))
    return state[2], "\n".join(map("".join, state[3]))
