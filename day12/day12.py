from __future__ import annotations
from os import path
from enum import Enum
from functools import reduce

class Action(Enum):
    MOVE_NORTH = 'N'
    MOVE_SOUTH = 'S'
    MOVE_EAST = 'E'
    MOVE_WEST = 'W'
    TURN_LEFT = 'L'
    TURN_RIGHT = 'R'
    MOVE_FORWARD = 'F'

    def __str__(self):
        return self.value

class Direction(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'

    def __str__(self):
        return self.value

    def rotate_left(self) -> Direction:
        dir_rotated_left = {
            Direction.NORTH: Direction.WEST,
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH
        }
        return dir_rotated_left[self]
    
    def rotate_right(self) -> Direction:
        dir_rotated_right = {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH
        }
        return dir_rotated_right[self]

ShipState = tuple[int, int, Direction]
ShipState_v2 = tuple[int, int, int, int]

class Instruction:
    def __init__(self, action: Action, arg: int):
        self.action = action
        self.arg = arg
    
    @staticmethod
    def parse(text: str) -> Instruction:
        action = Action(text[0])
        arg = int(text[1:])
        return Instruction(action, arg)

    def execute(self, curr_state: ShipState) -> ShipState:
        x, y, dir = curr_state

        if self.action == Action.MOVE_NORTH:
            y += self.arg
        elif self.action == Action.MOVE_SOUTH:
            y -= self.arg
        elif self.action == Action.MOVE_EAST:
            x += self.arg
        elif self.action == Action.MOVE_WEST:
            x -= self.arg
        elif self.action == Action.TURN_LEFT:
            n_times = self.arg // 90
            dir = reduce(lambda d, _: d.rotate_left(), range(n_times), dir)
        elif self.action == Action.TURN_RIGHT:
            n_times = self.arg // 90
            dir = reduce(lambda d, _: d.rotate_right(), range(n_times), dir)
        elif self.action == Action.MOVE_FORWARD:
            dir_to_action = {
                Direction.NORTH: Action.MOVE_NORTH,
                Direction.SOUTH: Action.MOVE_SOUTH,
                Direction.EAST: Action.MOVE_EAST,
                Direction.WEST: Action.MOVE_WEST
            }
            return Instruction(dir_to_action[dir], self.arg).execute((x, y, dir))
        else:
            raise NotImplementedError(f'Not implemented for {self.action}')

        return (x, y, dir)

    def execute_v2(self, curr_state: ShipState_v2) -> ShipState_v2:
        x, y, wp_dx, wp_dy = curr_state

        if self.action == Action.MOVE_NORTH:
            wp_dy += self.arg
        elif self.action == Action.MOVE_SOUTH:
            wp_dy -= self.arg
        elif self.action == Action.MOVE_EAST:
            wp_dx += self.arg
        elif self.action == Action.MOVE_WEST:
            wp_dx -= self.arg
        elif self.action == Action.TURN_LEFT:
            n_times = self.arg // 90
            wp_dx, wp_dy = reduce(lambda xy, _: (-xy[1], xy[0]), range(n_times), (wp_dx, wp_dy))
        elif self.action == Action.TURN_RIGHT:
            n_times = self.arg // 90
            wp_dx, wp_dy = reduce(lambda xy, _: (xy[1], -xy[0]), range(n_times), (wp_dx, wp_dy))
        elif self.action == Action.MOVE_FORWARD:
            x += wp_dx * self.arg
            y += wp_dy * self.arg
        else:
            raise NotImplementedError(f'Not implemented for {self.action}')

        return (x, y, wp_dx, wp_dy)


def parse_instructions(input_file: str) -> list[Instruction]:
    with open(input_file) as f:
        return [
            Instruction.parse(line)
            for line 
            in f.read().splitlines()
        ]

def navigate(curr_state: ShipState, insts: list[Instruction]) -> ShipState:
    if insts == []:
        return curr_state
    else:
        inst, *next_insts = insts
        new_state = inst.execute(curr_state)
        return navigate(new_state, next_insts)

def navigate_v2(curr_state: ShipState_v2, insts: list[Instruction]) -> ShipState_v2:
    if insts == []:
        return curr_state
    else:
        inst, *next_insts = insts
        new_state = inst.execute_v2(curr_state)
        return navigate_v2(new_state, next_insts)


def solve(input_file: str) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    insts = parse_instructions(full_path)
    tx, ty, _ = navigate((0, 0, Direction.EAST), insts)
    print('Part 1 answer:', abs(tx) + abs(ty))

    tx, ty, *_ = navigate_v2((0, 0, 10, 1), insts)
    print('Part 2 answer:', abs(tx) + abs(ty))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')