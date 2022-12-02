fmt_dict = {"sep": "\n\n"}


def solve(elves):
    sums = sorted((sum(map(int, elf.split("\n"))) for elf in elves), reverse=True)
    return sum(sums[:1]), sum(sums[:3])
