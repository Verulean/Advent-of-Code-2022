from timeit import timeit
import os


def aoc_input(file_name, input_dir="input", cast_type=str, strip=True, sep='\n', file_prefix=''):
    cwd = os.path.dirname(__file__)
    with open(os.path.join(cwd, input_dir, file_prefix + file_name), 'r') as f:
        if sep is None:
            return f.read()
        return [cast_type(i.strip()) if strip else cast_type(i) for i in f.read().split(sep=sep)]

def time_to_string(n, solve, data, pad=11):
    units = ((1e0, 's'), (1e-3, 'ms'), (1e-6, 'μs'), (1e-9, 'ns'))
    t = timeit(lambda: solve(data), number=n) / n
    
    for magnitude, unit in units:
        if t > magnitude:
            return f"{t/magnitude:.4f} {unit}".rjust(pad)