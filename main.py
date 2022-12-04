from datetime import datetime
from importlib import import_module
from pprint import pprint
from pytz import timezone
import aoc_util


DT_NOW = datetime.now(timezone("America/New_York"))
CURRENT_YEAR = DT_NOW.year
CURRENT_DAY = DT_NOW.day


def main(
    n=min(CURRENT_DAY, 25),
    time=False,
    n_trials=1000,
    print_solution=True,
    file_variant="",
):
    aoc = import_module(f"days.aoc{n:02}{file_variant}")
    fmt = getattr(aoc, "fmt_dict", {})
    data = aoc_util.aoc_input(n, **fmt)

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
    x = main()
