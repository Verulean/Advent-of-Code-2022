from datetime import datetime as dt
from importlib import import_module
from pprint import pprint
import pytz
import aoc_util


def current_day():
    EST = pytz.timezone("America/New_York")
    return dt.now(EST).day


def main(
    n=min(current_day(), 25),
    time=False,
    n_trials=1000,
    print_solution=True,
    file_variant="",
):
    aoc = import_module(f"days.aoc{n:02}{file_variant}")
    fmt = getattr(aoc, "fmt_dict", {})
    data = aoc_util.aoc_input(f"{n:02}.txt", **fmt)

    if time:
        t = aoc_util.time_to_string(n_trials, aoc.solve, data)
        if n_trials == 1:
            result = t
        else:
            result = f"average of {t} over {n_trials} runs."

        print(f"Day {str(n).rjust(2)}: {result}")

    solution = aoc.solve(data)
    if print_solution:
        pprint(solution)

    return solution


if __name__ == "__main__":
    x = main(4)
