class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.files = set()
        self.children = dict()

    def add_file(self, name, size):
        self.files.add((name, size))

    @property
    def total_size(self):
        return sum(f[1] for f in self.files) + sum(
            d.total_size for d in self.children.values()
        )

    def add_subdirectory(self, name):
        if name in self.children:
            return
        self.children[name] = Directory(name, self)

    def cd(self, child_name):
        if child_name == "..":
            return self.parent
        elif child_name == "/":
            return ROOT
        elif child_name not in self.children:
            self.add_subdirectory(child_name)
        return self.children[child_name]

    def part1(self):
        s = 0
        size = self.total_size
        if size <= 100_000:
            s += size
        for child in self.children.values():
            s += child.part1()
        return s

    def part2(self, space_needed=None):
        size = self.total_size
        if space_needed is None:
            space_needed = max(0, size - 4e7)
        best = None
        if size >= space_needed and (best is None or size < best):
            best = size
        for child in self.children.values():
            candidate = child.part2(space_needed)
            if candidate is not None and candidate < best:
                best = candidate
        return best


ROOT = Directory("/")


def solve(data):
    data = [line.split() for line in data]

    i = 0
    currdir = ROOT
    while i < len(data):
        line = data[i]
        if "$" in line[0]:
            cmd = line[1]
            if cmd == "cd":
                currdir = currdir.cd(line[2])
                i += 1
            elif cmd == "ls":
                i += 1
                a, b = data[i][:2]
                while (a.isnumeric() or a == "dir") and i < len(data):
                    a, b = data[i][:2]
                    if a.isnumeric():
                        currdir.add_file(b, int(a))
                        i += 1
                    elif a == "dir":
                        currdir.add_subdirectory(b)
                        i += 1

    return ROOT.part1(), ROOT.part2()
