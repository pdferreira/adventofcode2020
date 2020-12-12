from os import path
from typing import Optional
import day01.day1 as day1

def parse_xmas_numbers(input_file: str) -> list[int]:
    with open(input_file) as f:
        return [int(n) for n in f.readlines()]

def find_invalid_number(xmas_ns: list[int], window_size: int) -> Optional[int]:
    if len(xmas_ns) <= window_size:
        return None
    else:
        num_to_validate = xmas_ns[window_size]
        if day1.find_pair(xmas_ns[:window_size], num_to_validate):
            return find_invalid_number(xmas_ns[1:], window_size)
        else:
            return num_to_validate

def find_contiguous_sum(xmas_ns: list[int], expected_sum: int) -> Optional[list[int]]:
    # stack overflows, no tail recursion in Python!
    # sum_ns = find_contiguous_sum_rec(xmas_ns, [], 0, expected_sum)
    sum_ns = find_contiguous_sum_it(xmas_ns, expected_sum)
    if sum_ns and len(sum_ns) > 1:
        return sum_ns

def find_contiguous_sum_rec(xmas_ns: list[int], curr_sum_ns: list[int], curr_sum: int, expected_sum: int) -> Optional[list[int]]:
    if curr_sum == expected_sum:
        return curr_sum_ns
    
    if curr_sum < expected_sum and xmas_ns != []:
        # if we are below, add the next number
        next_n, *rest_xmas_ns = xmas_ns
        return find_contiguous_sum_rec(rest_xmas_ns, curr_sum_ns + [next_n], curr_sum + next_n, expected_sum)
    
    if curr_sum > expected_sum and curr_sum_ns != []:
        # if we are above, remove the oldest number
        oldest_n, *rest_curr_sum = curr_sum_ns
        return find_contiguous_sum_rec(xmas_ns, rest_curr_sum, curr_sum - oldest_n, expected_sum)

def find_contiguous_sum_it(xmas_ns: list[int], expected_sum: int) -> Optional[list[int]]:
    curr_sum_ns = []
    curr_sum = 0
    while True:
        if curr_sum == expected_sum:
            return curr_sum_ns
    
        if curr_sum < expected_sum and xmas_ns != []:
            # if we are below, add the next number
            next_n, *xmas_ns = xmas_ns
            curr_sum_ns.append(next_n)
            curr_sum += next_n

        elif curr_sum > expected_sum and curr_sum_ns != []:
            # if we are above, remove the oldest number
            oldest_n = curr_sum_ns.pop(0)
            curr_sum -= oldest_n

        else:
            break

       
def solve(input_file: str, window_size: int) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)
    xmas_ns = parse_xmas_numbers(full_path)

    invalid_n = find_invalid_number(xmas_ns, window_size)
    print('Part 1 answer:', invalid_n)

    if invalid_n:
        sum_ns = find_contiguous_sum(xmas_ns, invalid_n)
        if sum_ns:
            print(f'Part 2 answer: {min(sum_ns) + max(sum_ns)} (from {sum_ns})')
        else:
            print('No answer found for Part 2')
    
    print()

if __name__ == '__main__':
    solve('example.txt', window_size = 5)
    solve('input.txt', window_size = 25)