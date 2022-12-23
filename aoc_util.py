from importlib.util import module_from_spec, spec_from_file_location
from main import CURRENT_YEAR
from timeit import timeit
import os
import requests


CURRENT_WORKING_DIRECTORY = os.path.dirname(__file__)


def aoc_import(day, file_suffix, days_dir="days"):
    spec = spec_from_file_location(
        f"aoc{day:02}",
        os.path.join(
            CURRENT_WORKING_DIRECTORY, days_dir, f"aoc{day:02}{file_suffix}.py"
        ),
    )
    aoc = module_from_spec(spec)
    spec.loader.exec_module(aoc)
    return aoc


def aoc_input(
    day, input_dir="input", cast_type=str, strip=True, sep="\n", file_prefix=""
):
    file_path = os.path.join(
        CURRENT_WORKING_DIRECTORY, input_dir, f"{file_prefix}{day:02n}.txt"
    )
    if not os.path.exists(file_path):
        download_input(day, file_path)

    with open(file_path) as f:
        if sep is None:
            return f.read()
        return [
            cast_type(i.strip()) if strip else cast_type(i)
            for i in f.read().split(sep)
        ]


def download_input(day, path):
    url = f"https://adventofcode.com/{CURRENT_YEAR}/day/{day}/input"
    session_id = get_session_id()
    if session_id is None:
        return
    kwargs = {
        "headers": {
            "User-Agent": "github.com/Verulean/Advent-of-Code-2022 discord:@Verulean#7298"
        },
        "cookies": {"session": session_id},
    }
    response = requests.get(url, **kwargs)
    if not response.ok:
        raise RuntimeError(f"Request failed. {response.content}")
    with open(path, "w+") as f:
        f.write(response.text[:-1])


def get_session_id():
    with open("session.cookie") as f:
        return f.read().strip()
    return None


def time_to_string(n, solve, data, pad=11):
    units = ((1e0, "s"), (1e-3, "ms"), (1e-6, "μs"), (1e-9, "ns"))
    t = timeit(lambda: solve(data), number=n) / n

    for magnitude, unit in units:
        if t > magnitude:
            return f"{t/magnitude:.4f} {unit}".rjust(pad)
