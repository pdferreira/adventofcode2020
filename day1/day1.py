from os import path
from typing import Optional

def find_pair(num_array: list[int], expected_sum: int) -> Optional[tuple[int, int]]:
    expected_nums = set()
    for num in num_array:
        if num in expected_nums:
            return (num, expected_sum - num)
        else:
            expected_nums.add(expected_sum - num)

def solve_part1(num_array: list[int], expected_sum: int) -> int:
    (a, b) = find_pair(num_array, expected_sum) # type: ignore
    return a * b

def read_file(input_file: str) -> list[int]:
    full_path = path.join(path.dirname(__file__), input_file)
    with open(full_path) as f:
        return [int(line) for line in f.readlines()]

def find_triple(num_array: list[int], expected_sum: int) -> Optional[tuple[int, int, int]]:
    for idx, num in enumerate(num_array):
        sub_array = num_array[(idx + 1):]
        pair = find_pair(sub_array, expected_sum - num)
        if pair is not None:
            return (num,) + pair # type: ignore

def solve_part2(num_array, expected_sum):
    (a, b, c) = find_triple(num_array, expected_sum) # type: ignore
    return a * b * c

if __name__ == '__main__':
    num_array = read_file('input.txt')
    print('Part 1 answer:', solve_part1(num_array, 2020))
    print('Part 2 answer:', solve_part2(num_array, 2020))