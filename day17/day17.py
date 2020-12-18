from __future__ import annotations
from os import path
from typing import Optional
from functools import reduce
from dataclasses import dataclass
from collections.abc import Iterator
import time

CubeState = bool

@dataclass(frozen = True, order = True)
class Coord:
    x: int
    y: int
    z: int
    w: int

    def __add__(self, other: Coord) -> Coord:
        return Coord(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)

    def __sub__(self, other: Coord) -> Coord:
        return Coord(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)

@dataclass
class PocketDimension:
    active_cubes: set[Coord]
    origin: Coord # lower x,y,z,w corner of the known map
    dest: Coord # opposite corner to `origin` 

    @staticmethod
    def parse_initial_state(input_str: str) -> PocketDimension:
        active_cubes = set[Coord]()

        for y, line in enumerate(input_str.splitlines()):
            for x, c in enumerate(line):
                if c == '#':
                    active_cubes.add(Coord(x, y, 0, 0))
 
        max_x = max(c.x for c in active_cubes)
        max_y = max(c.y for c in active_cubes)

        dest = Coord(max_x + 1, max_y + 1, 1, 1)
        origin = Coord(0, 0, 0, 0)
        return PocketDimension(active_cubes, origin, dest)

    def __getitem__(self, coord: Coord) -> CubeState:
        return coord in self.active_cubes

    def __str__(self) -> str:
        lines = list[str]()

        for w in range(self.origin.w, self.dest.w):
            for z in range(self.origin.z, self.dest.z):
                lines.append(f'z={z}, w={w}')
                for y in range(self.origin.y, self.dest.y):
                    cubes = [
                        '#' if Coord(x, y, z, w) in self.active_cubes else '.'
                        for x 
                        in range(self.origin.x, self.dest.x)
                    ]
                    lines.append(''.join(cubes))
                else:
                    lines.append('')

        return '\n'.join(lines)

def parse_initial_state(input_file: str) -> PocketDimension:
    with open(input_file) as f:
        return PocketDimension.parse_initial_state(f.read())

def get_neighbor_cube_states(dim: PocketDimension, coord: Coord, use_4d: bool) -> Iterator[CubeState]:
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dw in [-1, 0, 1] if use_4d else [0]:
                    if (dx, dy, dz, dw) == (0, 0, 0, 0):
                        continue

                    neighbor_coord = Coord(dx, dy, dz, dw) + coord
                    yield dim[neighbor_coord]

def get_new_state(dim: PocketDimension, coord: Coord, use_4d: bool) -> CubeState:
    curr_state = dim[coord]
    num_active_neighbors = sum(1 for state in get_neighbor_cube_states(dim, coord, use_4d) if state)

    if curr_state and num_active_neighbors not in [2, 3]:
        return False

    if not curr_state and num_active_neighbors == 3:
        return True

    return curr_state

def simulate_cycle(dim: PocketDimension, use_4d: bool) -> PocketDimension:
    new_active_cubes = set[Coord](
        Coord(x, y, z, w)
        for x in range(dim.origin.x - 1, dim.dest.x + 1)
        for y in range(dim.origin.y - 1, dim.dest.y + 1)
        for z in range(dim.origin.z - 1, dim.dest.z + 1)
        for w in range(dim.origin.w - 1, dim.dest.w + 1)
        if get_new_state(dim, Coord(x, y, z, w), use_4d)
    )
    
    # calculate the new boundaries for reference
    min_x, *_, max_x = sorted(c.x for c in new_active_cubes)
    min_y, *_, max_y = sorted(c.y for c in new_active_cubes)
    min_z, *_, max_z = sorted(c.z for c in new_active_cubes)
    min_w, *_, max_w = sorted(c.w for c in new_active_cubes)

    new_origin = Coord(min_x, min_y, min_z, min_w)
    new_dest = Coord(max_x + 1, max_y + 1, max_z + 1, max_w + 1)
    new_dim = PocketDimension(new_active_cubes, new_origin, new_dest)
    return new_dim

def solve(input_file: str, *, expected: tuple[Optional[int], Optional[int]] = (None, None)) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    pocket_dimension = parse_initial_state(full_path)

    # Part 1
    start_p1 = time.time_ns()
    # print(pocket_dimension)
    final_dim_p1 = reduce(lambda dim, _: simulate_cycle(dim, use_4d = False), range(6), pocket_dimension)
    obtained_p1 = len(final_dim_p1.active_cubes)

    print('Part 1 answer:', obtained_p1, '(took', time.time_ns() - start_p1, 'ns)')
    if expected[0] is not None and expected[0] != obtained_p1:
        print('Expected:', expected[0])

    # Part 2
    start_p2 = time.time_ns()
    final_dim_p2 = reduce(lambda dim, _: simulate_cycle(dim, use_4d = True), range(6), pocket_dimension)
    obtained_p2 = len(final_dim_p2.active_cubes)

    print('Part 2 answer:', obtained_p2, '(took', time.time_ns() - start_p2, 'ns)')
    if expected[1] is not None and expected[1] != obtained_p2:
        print('Expected:', expected[1])

    print()

if __name__ == '__main__':
    solve('example.txt', expected = (112, 848))
    solve('input.txt', expected = (276, 2136))