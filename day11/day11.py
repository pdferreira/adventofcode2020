from os import path
from typing import Callable, Iterator, Optional
from enum import Enum

class Position(Enum):
    FLOOR = '.'
    EMPTY_SEAT = 'L'
    OCCUPIED_SEAT = '#'

    def __str__(self):
        return self.value

SeatLayout = list[list[Position]]
ApplySeatingRulesFn = Callable[[SeatLayout, int, int], Position]

def parse_seat_layout(input_file: str) -> SeatLayout:
    with open(input_file) as f:
        return [
            [Position(pos) for pos in line]
            for line 
            in f.read().splitlines()
        ]

def print_seat_layout(seat_layout: SeatLayout):
    for seat_line in seat_layout:
        print(*seat_line, sep = '')

def apply_seating_rules_p1(seat_layout: SeatLayout, row: int, col: int) -> Position:
    nearby_occupied_seats = count_nearby_occupied_seats(seat_layout, row, col)
    
    pos = seat_layout[row][col]
    if pos == Position.EMPTY_SEAT and nearby_occupied_seats == 0:
        return Position.OCCUPIED_SEAT
    elif pos == Position.OCCUPIED_SEAT and nearby_occupied_seats >= 4:
        return Position.EMPTY_SEAT
    else:
        return pos

def get_nearby_seats(seat_layout: SeatLayout, center_row: int, center_col: int) -> Iterator[Position]:
    for row in yield_axis_var(center_row, len(seat_layout), radius = 1):
        seat_line = seat_layout[row]

        for col in yield_axis_var(center_col, len(seat_line), radius = 1):
            if col == center_col and row == center_row:
                continue
            else:
                yield seat_line[col]

def count_nearby_occupied_seats(seat_layout: SeatLayout, center_row: int, center_col: int) -> int:
    nearby_seats = list(get_nearby_seats(seat_layout, center_row, center_col))
    return nearby_seats.count(Position.OCCUPIED_SEAT)

def apply_seating_rules_p2(seat_layout: SeatLayout, row: int, col: int) -> Position:
    visible_occupied_seats = count_visible_occupied_seats(seat_layout, row, col)
    
    pos = seat_layout[row][col]
    if pos == Position.EMPTY_SEAT and visible_occupied_seats == 0:
        return Position.OCCUPIED_SEAT
    elif pos == Position.OCCUPIED_SEAT and visible_occupied_seats >= 5:
        return Position.EMPTY_SEAT
    else:
        return pos

def find_next_seat(seat_layout: SeatLayout, curr_row: int, curr_col: int, dr: int, dc: int) -> Optional[Position]:
    new_row = curr_row + dr
    new_col = curr_col + dc
    if 0 <= new_row < len(seat_layout):
        seat_line = seat_layout[new_row]
        if 0 <= new_col < len(seat_line):
            pos = seat_line[new_col]
            if pos != Position.FLOOR:
                return pos
            else:
                return find_next_seat(seat_layout, new_row, new_col, dr, dc)

def get_cardinal_visible_seats(seat_layout: SeatLayout, center_row: int, center_col: int) -> Iterator[Position]:
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            
            pos = find_next_seat(seat_layout, center_row, center_col, dr, dc)
            if pos is not None:
                yield pos

def count_visible_occupied_seats(seat_layout: SeatLayout, center_row: int, center_col: int) -> int:
    visible_seats = list(get_cardinal_visible_seats(seat_layout, center_row, center_col))
    return visible_seats.count(Position.OCCUPIED_SEAT)

def yield_axis_var(center: int, limit: int, radius: int) -> Iterator[int]:
    if center - radius >= 0:
        yield center - radius
    
    yield center

    if center + radius < limit:
        yield center + radius

def simulate_seating_round(seat_layout: SeatLayout, apply_rules_fn: ApplySeatingRulesFn) -> SeatLayout:
    return [
        [
            apply_rules_fn(seat_layout, row, col)
            for col
            in range(len(seat_layout[0]))
        ]
        for row
        in range(len(seat_layout))
    ]

def simulate_seating(seat_layout: SeatLayout, apply_rules_fn: ApplySeatingRulesFn, debug: bool = False) -> SeatLayout:
    i = 0
    if debug:
        print('Iteration #', i)
        print_seat_layout(seat_layout)
        print()

    while True:
        new_seat_layout = simulate_seating_round(seat_layout, apply_rules_fn)
        if new_seat_layout == seat_layout:
            break
        else:
            seat_layout = new_seat_layout

        if debug:
            i += 1
            print('Iteration #', i)
            print_seat_layout(seat_layout)
            print()
        
    return new_seat_layout

def count_occupied_seats(seat_layout: SeatLayout) -> int:
    if seat_layout == []:
        return 0
    else:
        first_line, *other_lines = seat_layout
        return first_line.count(Position.OCCUPIED_SEAT) + count_occupied_seats(other_lines)

def solve(input_file: str) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    seat_layout = parse_seat_layout(full_path)
    final_seat_layout_p1 = simulate_seating(seat_layout, apply_seating_rules_p1)

    print('Part 1 answer:', count_occupied_seats(final_seat_layout_p1))

    final_seat_layout_p2 = simulate_seating(seat_layout, apply_seating_rules_p2)
    print('Part 2 answer:', count_occupied_seats(final_seat_layout_p2))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')