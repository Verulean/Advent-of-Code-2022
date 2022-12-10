def step(state, value=0):
    i, j = divmod(state[0] - 1, 40)
    if j == 0 and i > 0:
        state[3] += "\n"
    state[3] += (".", "#")[abs(j - state[1]) <= 1]
    state[0] += 1
    state[1] += value
    if state[0] % 40 == 20:
        state[2] += state[0] * state[1]


def solve(instructions):
    state = [1, 1, 0, ""]
    for instr in instructions:
        _, *n = instr.split()
        step(state)
        if n:
            step(state, int(n[0]))
    return state[2], state[3]
