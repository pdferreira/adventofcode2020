from __future__ import annotations
from os import path
from itertools import islice
from typing import Optional
from collections import deque
import time

Deck = list[int]

def parse_decks(input_file: str) -> list[Deck]:
    with open(input_file) as f:
        deck_strs = f.read().split('\n\n')
        return [parse_deck(s) for s in deck_strs]

def parse_deck(deck_str: str) -> Deck:
    lines = deck_str.splitlines()
    return [int(line) for line in lines[1:]]

def play_combat(decks: list[Deck]) -> tuple[int, Deck]:
    players = [deque(d) for d in decks]

    # while there are at least two players with cards
    while len([p for p in players if len(p) > 0]) > 1:
        plays = [(p.popleft(), p) for p in players if len(p) > 0]

        sorted_plays = sorted(plays, reverse = True)
        _, winning_p = sorted_plays[0]
        for num, _ in sorted_plays:
            winning_p.append(num)

    return next((idx, list(p)) for idx, p in enumerate(players) if len(p) > 0)

def play_recursive_combat(decks: list[Deck]) -> tuple[int, Deck]:
    players = [deque(d) for d in decks]
    previous_states = list[list[deque[int]]]()

    # while there are at least two players with cards
    while len([p for p in players if len(p) > 0]) > 1:
        # if this state already appeared, player 1 wins instantly
        curr_state = [p.copy() for p in players]
        if curr_state in previous_states:
            return 0, list(players[0])
        else:
            previous_states.append(curr_state)

        # otherwise, draw the cards from the top of each deck
        plays = [(p.popleft(), p) for p in players if len(p) > 0]

        # if all have enough cards left, enter a new recursive combat
        # otherwise the highest wins
        if all(len(p) >= num for num, p in plays):
            rec_winner_idx, _ = play_recursive_combat([list(islice(p, num)) for num, p in plays])
            winning_num, winning_p = plays[rec_winner_idx]
        else:
            winning_num, winning_p = max(plays)

        # add the winning first and the rest sorted (not in the game rules, but trying to generalize to 3+ players)
        winning_p.append(winning_num)
        for num, _ in sorted(plays, reverse = True):
            if num != winning_num:
                winning_p.append(num)

    return next((idx, list(p)) for idx, p in enumerate(players) if len(p) > 0)
        

def get_score(deck: Deck) -> int:
    return sum(
        (idx + 1) * num
        for idx, num
        in enumerate(deck[::-1])
    )
    
def solve(input_file: str, *, expected: tuple[Optional[int], Optional[int]] = (None, None), skip_part1: bool = False) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    # Common
    start_common = time.time_ns()
    decks = parse_decks(full_path)
    time_common = time.time_ns() - start_common

    # Part 1
    if not skip_part1:
        start_p1 = time.time_ns()
        _, winner_deck = play_combat(decks)
        print(winner_deck)
        obtained_p1 = get_score(winner_deck)
        time_p1 = (time.time_ns() - start_p1) + time_common

        print('Part 1 answer:', obtained_p1, '(took', time_p1, 'ns)')
        if expected[0] is not None and expected[0] != obtained_p1:
            print('Expected:', expected[0])

    # Part 2
    start_p2 = time.time_ns()
    _, winner_deck_p2 = play_recursive_combat(decks)
    print(winner_deck_p2)
    obtained_p2 = get_score(winner_deck_p2)
    time_p2 = (time.time_ns() - start_p2) + time_common

    print('Part 2 answer:', obtained_p2, '(took', time_p2, 'ns)')
    if expected[1] is not None and expected[1] != obtained_p2:
        print('Expected:', expected[1])

    print()

if __name__ == '__main__':
    solve('example.txt', expected = (306, 291))
    solve('example2.txt', expected = (None, 105), skip_part1 = True) # part 1 doesn't handle loops
    solve('input.txt', expected = (30138, 31587))