import numpy as np


class CRT:
    def __init__(self):
        self.__x = 1
        self.__cycle = 1
        self.__signal_sum = 0
        self.__screen = np.full((6, 40), ".")
    
    def parse(self, instr):
        match instr.split():
            case ["addx", n]:
                self.__increment()
                self.__increment(int(n))
            case ["noop"]:
                self.__increment()
            case _:
                raise ValueError(f"Invalid instruction: '{instr}'.")
    
    def __increment(self, value=0):
        i, j = divmod(self.__cycle - 1, 40)
        if abs(j - self.__x) <= 1:
            self.__screen[i, j] = "#"
        self.__cycle += 1
        self.__x += value
        if (self.__cycle - 20) % 40 == 0:
            self.__signal_sum += self.__cycle * self.__x
    
    @property
    def signal_strength(self):
        return self.__signal_sum
    
    @property
    def screen(self):
        return "\n".join("".join(row) for row in self.__screen)
                
def solve(data):
    Screen = CRT()
    for line in data:
        Screen.parse(line)
    return Screen.signal_strength, Screen.screen
