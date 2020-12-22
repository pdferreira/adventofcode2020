from __future__ import annotations
from os import path
from itertools import takewhile
from functools import reduce
from typing import Optional
import time
import re

class Tile:
    id: int
    content: list[str]
    sides: list[str]
    flipped_sides: list[str]
    num_flips: int = 0

    def __init__(self, id: int, content: list[str]):
        self.id = id
        self.content = content
        self.sides = [
            content[0], # TOP side
            ''.join(line[-1] for line in content), # right side
            content[-1][::-1], # BOTTOM side
            ''.join(line[0] for line in content[::-1]) # left side
        ]
        self.flipped_sides = [
            self.sides[0][::-1],
            self.sides[3][::-1], # switch left and right
            self.sides[2][::-1],
            self.sides[1][::-1]
        ]

TILE_ID_PATTERN = re.compile(r'Tile (\d+):')

def parse_tiles(input_file: str) -> list[Tile]:
    with open(input_file) as f:
        it = iter(f.read().splitlines())
        tiles = list[Tile]()
        while True:
            next_line = next(it, None)
            if next_line:
                match = TILE_ID_PATTERN.fullmatch(next_line)
                if match:
                    tile_id = int(match.group(1))
                    tile = list(takewhile(lambda line: line != "", it))
                    tiles.append(Tile(tile_id, tile))
                    # print(tiles[-1].id, tiles[-1].sides)
                    continue
            break
        
        return tiles

def match_tiles(tiles: list[Tile]) -> dict[Tile, list[Tile]]:
    tile_matches = dict[Tile, list[Tile]]()
    for t1 in tiles:
        tile_matches[t1] = list()
        for t2 in tiles:
            if t1 == t2:
                continue

            if set(t1.sides) & set(t2.sides):
                tile_matches[t1].append(t2)
            elif set(t1.flipped_sides) & set(t2.sides):
                tile_matches[t1].append(t2)

    return tile_matches

def get_corner_tiles(tile_matches: dict[Tile, list[Tile]]) -> list[Tile]:
    return [t for t in tile_matches if len(tile_matches[t]) == 2]

def solve(input_file: str, *, expected: tuple[Optional[int], Optional[int]] = (None, None)) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    # Common
    start_common = time.time_ns()
    tiles = parse_tiles(full_path)
    time_common = time.time_ns() - start_common

    # Part 1
    start_p1 = time.time_ns()
    tile_matches = match_tiles(tiles)
    corner_tiles = get_corner_tiles(tile_matches)
    assert len(corner_tiles) == 4
    time_p1 = (time.time_ns() - start_p1) + time_common
    obtained_p1 = reduce(lambda acc, t: acc * t.id, corner_tiles, 1)

    print('Part 1 answer:', obtained_p1, '(took', time_p1, 'ns)')
    if expected[0] is not None and expected[0] != obtained_p1:
        print('Expected:', expected[0])

    print()

if __name__ == '__main__':
    solve('example.txt', expected = (20899048083289, None))
    solve('input.txt', expected = (17712468069479, None))