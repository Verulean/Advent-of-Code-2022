from copy import deepcopy
from util import chunks, ints


fmt_dict = {
    "strip": False,
    "sep": "\n\n",
}


class CrateStack:
    def __init__(self, width):
        self.__stack = tuple([] for _ in range(width))

    @classmethod
    def from_string(cls, msg):
        lines = msg.split("\n")
        stack = cls(ints(lines[-1])[-1])
        for row in lines[-2::-1]:
            for i, chunk in enumerate(chunks(row, 4)):
                crate = chunk[1]
                if crate.isalpha():
                    stack.push(i, crate)
        return stack

    def push(self, index, value):
        self.__stack[index].append(value)

    def move(self, count, source, dest, simultaneous=False):
        crates = self.__stack[source - 1][-count:]
        del self.__stack[source - 1][-count:]
        if not simultaneous:
            crates = reversed(crates)
        self.__stack[dest - 1].extend(crates)

    @property
    def message(self):
        return "".join(col[-1] if col else "" for col in self.__stack)


def solve(data):
    stack1 = CrateStack.from_string(data[0])
    stack2 = deepcopy(stack1)

    for instr in map(ints, data[1].split("\n")):
        stack1.move(*instr)
        stack2.move(*instr, simultaneous=True)

    return stack1.message, stack2.message
