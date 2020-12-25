from __future__ import annotations
from typing import Optional
import time

def transform(subject_nr: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject_nr
        value %= 20201227
    return value

def find_loop_size(subject_nr: int, public_key: int) -> int:
    loop_size = 0
    value = public_key
    while value != 1:
        loop_size += 1
        while value % subject_nr > 0:
            value += 20201227
        value /= subject_nr

    return loop_size

def solve(*, subject_nr: int, public_keys: tuple[int, int], expected: Optional[int] = None) -> None:
    print(f'[Subject={subject_nr}, Public Keys={public_keys}]')

    # Part 1
    start_p1 = time.time_ns()
    loop_sizes = tuple([find_loop_size(subject_nr, key) for key in public_keys])
    print(loop_sizes)
    obtained_p1 = transform(public_keys[0], loop_sizes[1])
    time_p1 = time.time_ns() - start_p1

    print('Part 1 answer:', obtained_p1, '(took', time_p1, 'ns)')
    if expected is not None and expected != obtained_p1:
        print('Expected:', expected)

    print()

if __name__ == '__main__':
    solve(subject_nr = 7, public_keys = (5764801, 17807724), expected = 14897079)
    solve(subject_nr = 7, public_keys = (8335663, 8614349), expected = 6408263)