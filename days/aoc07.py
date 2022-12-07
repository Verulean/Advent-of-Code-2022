from collections import defaultdict


def parse_directories(directory_sizes, size_threshold, needed_space, total_space):
    small_dir_total = 0
    best_freed_size = total_space
    
    minimum_size = directory_sizes[("/",)] + needed_space - total_space
    for size in directory_sizes.values():
        if size <= size_threshold:
            small_dir_total += size
        if minimum_size <= size < best_freed_size:
            best_freed_size = size
    return small_dir_total, best_freed_size
        

def solve(data):
    sizes = defaultdict(int)
    processed_files = defaultdict(set)
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
                if a.isnumeric():
                    if not processing or b in processed_files[tuple(path)]:
                        continue
                    processed_files[tuple(path)].add(b)
                    file_size = int(a)
                    for i in range(len(path)):
                        sizes[tuple(path[: i + 1])] += file_size
    return parse_directories(sizes, 100_000, 30_000_000, 70_000_000)
