from collections import defaultdict


def solve(data):
    sizes = defaultdict(int)
    processing = False
    path = []
    for line in data:
        match line.split():
            case ["$", "cd", dirname]:
                processing = False
                match dirname:
                    case "..":
                        path.pop()
                    case "/":
                        path = ["/"]
                    case _:
                        path.append(dirname)
            case ["$", "ls"]:
                processing = True
            case [a, b]:
                if processing and a.isnumeric():
                    file_size = int(a)
                    for i in range(len(path)):
                        sizes[tuple(path[: i + 1])] += file_size
    ans1 = 0
    ans2 = 7e7
    needed_space = sizes[("/",)] - 4e7
    for directory, size in sizes.items():
        if size <= 100_000:
            ans1 += size
        if needed_space <= size < ans2:
            ans2 = size
    return ans1, ans2
