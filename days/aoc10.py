from dataclasses import dataclass


@dataclass
class State:
    cycle: int
    x: int
    signal_sum: int
    screen: str

    def step(self, value=0):
        i, j = divmod(self.cycle - 1, 40)
        if j == 0 and i > 0:
            self.screen += "\n"
        self.screen += (".", "#")[abs(j - self.x) <= 1]
        self.cycle += 1
        self.x += value
        if self.cycle % 40 == 20:
            self.signal_sum += self.cycle * self.x


def solve(data):
    state = State(1, 1, 0, "")
    for line in data:
        _, *n = line.split()
        state.step()
        if n:
            state.step(int(n[0]))
    return state.signal_sum, state.screen
