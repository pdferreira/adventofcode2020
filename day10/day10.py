from os import path
from typing import Literal, Optional, cast
from functools import reduce

JoltageDiff = Literal[1, 2, 3]

def parse_output_jolts(input_file: str) -> list[int]:
    with open(input_file) as f:
        return [int(n) for n in f.readlines()]

def get_jolt_differences(jolt_list: list[int]) -> list[JoltageDiff]:
    sorted_list = sorted(jolt_list)
    return cast(list[JoltageDiff], [
        b - a
        for a, b
        in zip(sorted_list[:-1], sorted_list[1:])
    ])

def get_e2e_jolt_differences(jolt_list: list[int]) -> list[JoltageDiff]:
    outlet_joltage = 0
    device_joltage = max(jolt_list) + 3
    return get_jolt_differences([outlet_joltage] + jolt_list + [device_joltage])


def solve_part1(jolt_diffs: list[JoltageDiff]) -> int:
    return jolt_diffs.count(1) * jolt_diffs.count(3)

def get_contiguous_jolt_differences(jolt_diffs: list[JoltageDiff]) -> list[tuple[JoltageDiff, int]]:
    '''Get the counts of sequences of the same jolt difference'''
    if jolt_diffs == []:
        return []
        
    counts = [(jolt_diffs[0], cast(int, 1))]
    
    for diff in jolt_diffs[1:]:
        (last_diff, n) = counts.pop()
        if last_diff == diff:
            counts.append((last_diff, n + 1))
        else:
            counts.append((last_diff, n))
            counts.append((diff, 1))

    return counts

def count_distinct_adapter_sequences(jolt_diffs: list[JoltageDiff]) -> int:
    contiguous_diffs = get_contiguous_jolt_differences(jolt_diffs)
    # ^^^
    # So the input only seems to contain 1 and 3 diffs, no 2s, and the max sequence is 4
    # Considering that, it's possible to work out by hand that...
    one_variations_per_seq_len = {
        1: 1,
        2: 2,
        3: 4,
        4: 7   # e.g. four 1s in a row, can be arranged in seven ways
    }
    
    def calc_num_sequences(total: int, diff_seq_pair: tuple[JoltageDiff, int]) -> int:
        diff, n = diff_seq_pair
        if diff == 3:
            return total
        elif diff == 1:
            if n in one_variations_per_seq_len:
                return total * one_variations_per_seq_len[n]
            else:
                raise NotImplementedError(f'Case for sequences of len {n} is not covered')
        else:
            raise NotImplementedError(f'Case for sequences of {diff}s is not covered')

    return reduce(calc_num_sequences, contiguous_diffs, 1)

       
def solve(input_file: str) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    jolt_list = parse_output_jolts(full_path)
    jolt_diffs = get_e2e_jolt_differences(jolt_list)
    
    print('Part 1 answer:', jolt_diffs.count(1) * jolt_diffs.count(3))
    print('Part 2 answer:', count_distinct_adapter_sequences(jolt_diffs))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('example2.txt')
    solve('input.txt')