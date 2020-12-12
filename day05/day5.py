from os import path
from typing import Optional
import re

class Coord:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

def parse_seat_coords(input_file: str) -> list[Coord]:
    with open(input_file) as f:
        return [
            parse_seat_coord(coord_code)
            for coord_code
            in f.readlines()]
        
def parse_seat_coord(coord_code: str) -> Coord:
    return Coord(
        row = row_code_to_number(coord_code[:7]),
        col = col_code_to_number(coord_code[7:])
    )

def row_code_to_number(row_code: str):
    row_binary = row_code.replace('F', '0').replace('B', '1')
    return int(row_binary, 2)

def col_code_to_number(col_code: str):
    col_binary = col_code.replace('L', '0').replace('R', '1')
    return int(col_binary, 2)

def calculate_seat_id(seat_coord: Coord):
    return seat_coord.row * 8 + seat_coord.col

def find_empty_seat(seat_ids: list[int]) -> Optional[int]:
    sorted_seats = sorted(seat_ids)
    prev_seat_id = sorted_seats[0]
    for seat_id in sorted_seats[1:]:
        if seat_id - prev_seat_id > 1:
            return seat_id - 1
        else:
            prev_seat_id = seat_id

def solve(input_file: str):
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)
    seat_coords = parse_seat_coords(full_path)
    seat_ids = [calculate_seat_id(c) for c in seat_coords]
    print('Part 1 answer:', max(seat_ids))
    print('Part 2 answer:', find_empty_seat(seat_ids))
    print()

def parse_seat_ids(input_file: str) -> list[int]:
    # seat_id can be taken directly by parsing the full coordinate as binary
    with open(input_file) as f:
        binary_coords = re.sub(
            r'\w',
            lambda m: '0' if m.group(0) in ['F', 'L'] else '1',
            f.read())
        return [int(c, 2) for c in binary_coords.splitlines()]

def solve_take2(input_file: str):
    print(f'[{input_file}] v2')
    full_path = path.join(path.dirname(__file__), input_file)
    seat_ids = parse_seat_ids(full_path)
    print('Part 1 answer:', max(seat_ids))
    print('Part 2 answer:', find_empty_seat(seat_ids))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')
    solve_take2('example.txt')
    solve_take2('input.txt')