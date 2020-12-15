from itertools import islice
from typing import Iterator, Optional
import time
    
def play_game(starting_nums: list[int]) -> Iterator[int]:
    last_spoken_in_turn = dict[int, int]()

    # initialize state with starting numbers and speak them
    *first_nums, last_num = starting_nums
    
    for idx, num in enumerate(first_nums):
        last_spoken_in_turn[num] = idx
        yield num

    prev_turn = len(first_nums)
    last_spoken_num = last_num
    yield last_num

    # from then on, play the game by the rules
    while True:
        # if it was spoken before the last turn, when was it?
        if last_spoken_num in last_spoken_in_turn:
            next_num = prev_turn - last_spoken_in_turn[last_spoken_num]
        else:
            next_num = 0

        # update the last spoken turns info after we figure out the next turn
        last_spoken_in_turn[last_spoken_num] = prev_turn
        
        # speak the next, but don't register its turn yet
        yield next_num
        last_spoken_num = next_num
        prev_turn += 1

def solve(starting_nums: list[int], *, expected: tuple[Optional[int], Optional[int]] = (None, None)) -> None:
    print(starting_nums)

    start_p1 = time.time_ns()
    *turns, last_turn = islice(play_game(starting_nums), 2020)
    print('Part 1 answer:', last_turn, '(took', time.time_ns() - start_p1, 'ns)')
    if expected[0] is not None and last_turn != expected[0]:
        print('Expected: ', expected[0])

    start_p2 = time.time_ns()
    *turns, last_turn = islice(play_game(starting_nums), 30000000)
    print('Part 2 answer:', last_turn, '(took', time.time_ns() - start_p2, 'ns)')
    if expected[1] is not None and last_turn != expected[1]:
        print('Expected: ', expected[1])

    print()

if __name__ == '__main__':
    solve([0, 3, 6], expected = (436, 175594))
    solve([1, 3, 2], expected = (1, 2578))
    solve([2, 1, 3], expected = (10, 3544142))
    solve([1, 2, 3], expected = (27, 261214))
    solve([2, 3, 1], expected = (78, 6895259))
    solve([3, 2, 1], expected = (438, 18))
    solve([3, 1, 2], expected = (1836, 362))
    solve([1, 0, 16, 5, 17, 4], expected = (1294, None))