from __future__ import annotations
from collections import defaultdict
from os import path
from enum import Enum
from typing import Optional
from collections.abc import Iterator
import time
import re

DIRECTION_PATTERN = re.compile(r'e|se|sw|w|nw|ne')

class Direction(Enum):
    EAST = 'e'
    SOUTH_EAST = 'se'
    SOUTH_WEST = 'sw'
    WEST = 'w'
    NORTH_WEST = 'nw'
    NORTH_EAST = 'ne'

def parse_directions(input_file: str) -> list[list[Direction]]:
    with open(input_file) as f:
        return [parse_direction_list(line) for line in f.read().splitlines()]

def parse_direction_list(line: str) -> list[Direction]:
    return [Direction(match) for match in DIRECTION_PATTERN.findall(line)]

def directions_to_coordinate(directions: list[Direction], start_coord = (0, 0, 0)) -> tuple[int, int, int]:
    if directions == []:
        return start_coord
    
    e, ne, se = start_coord
    d, *ds = directions
    new_coord = (lambda d: {
        Direction.EAST: (e, ne - 1, se - 1),
        Direction.WEST: (e, ne + 1, se + 1),
        Direction.SOUTH_EAST: (e + 1, ne - 1, se),
        Direction.NORTH_WEST: (e - 1, ne + 1, se),
        Direction.NORTH_EAST: (e - 1, ne, se - 1),
        Direction.SOUTH_WEST: (e + 1, ne, se + 1)
    }[d])(d)

    return directions_to_coordinate(ds, new_coord)


def flip_tiles(black_tiles: set[tuple[int, int, int]], tiles_to_flip: list[tuple[int, int, int]]):
    for coord in tiles_to_flip:
        if coord in black_tiles:
            # print('Flipping black -> white', coord)
            black_tiles.remove(coord)
        else:
            # print('Flipping white -> black', coord)
            black_tiles.add(coord)

def get_neighbor_coords(coord: tuple[int, int, int]) -> Iterator[tuple[int, int, int]]:
    for d in Direction:
        yield directions_to_coordinate([d], coord)

def daily_flip_tiles(black_tiles: set[tuple[int, int, int]]):
    tiles_to_flip = list[tuple[int, int, int]]()
    white_tiles_b_neighbors = defaultdict[tuple[int, int, int], int](lambda: 0)

    for tile_coord in black_tiles:
        num_black_neighbors = 0
        for coord in get_neighbor_coords(tile_coord):
            if coord in black_tiles:
                num_black_neighbors += 1
            else:
                white_tiles_b_neighbors[coord] += 1
        
        if num_black_neighbors == 0 or num_black_neighbors > 2:
            tiles_to_flip.append(tile_coord)

    for tile_coord, num_black_neighbors in white_tiles_b_neighbors.items():
        if num_black_neighbors == 2:
            tiles_to_flip.append(tile_coord)

    flip_tiles(black_tiles, tiles_to_flip)

def solve(input_file: str, *, expected: tuple[Optional[int], Optional[int]] = (None, None)) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    # Common
    start_common = time.time_ns()
    tiles_to_flip = parse_directions(full_path)
    time_common = time.time_ns() - start_common

    # Part 1
    start_p1 = time.time_ns()
    black_tiles = set[tuple[int, int, int]]()
    flip_tiles(black_tiles, [directions_to_coordinate(ds) for ds in tiles_to_flip])
    obtained_p1 = len(black_tiles)
    time_p1 = (time.time_ns() - start_p1) + time_common

    print('Part 1 answer:', obtained_p1, '(took', time_p1, 'ns)')
    if expected[0] is not None and expected[0] != obtained_p1:
        print('Expected:', expected[0])

    # Part 2
    start_p2 = time.time_ns()
    for _ in range(100):
        daily_flip_tiles(black_tiles)

    obtained_p2 = len(black_tiles)
    time_p2 = (time.time_ns() - start_p2) + time_common

    print('Part 2 answer:', obtained_p2, '(took', time_p2, 'ns)')
    if expected[1] is not None and expected[1] != obtained_p2:
        print('Expected:', expected[1])

    print()

if __name__ == '__main__':
    solve('example.txt', expected = (10, 2208))
    solve('input.txt', expected = (438, 4038))