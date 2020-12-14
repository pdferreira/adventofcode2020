from __future__ import annotations
from abc import ABC
from os import path
from typing import Iterator
import re
import time
    
class Instruction(ABC):
    pass

class UpdateMask(Instruction):
    def __init__(self, mask_str: str):
        self.raw_mask = mask_str
        self.and_mask = self._parse_zero_mask(mask_str)
        self.or_mask = self._parse_one_mask(mask_str)

    @staticmethod
    def _parse_zero_mask(mask_str: str) -> int:
        return int(mask_str.replace('X', '1'), 2)

    @staticmethod
    def _parse_one_mask(mask_str: str) -> int:
        return int(mask_str.replace('X', '0'), 2)

class UpdateMemory(Instruction):
    def __init__(self, mem_pos: int, value: int):
        self.mem_pos = mem_pos
        self.value = value
    
def parse_instructions(input_file: str) -> list[Instruction]:
    with open(input_file) as f:
        return [
            parse_instruction(line)
            for line 
            in f.read().splitlines()
        ]

MEM_REGEX = re.compile(r'mem\[(\d+)\]')

def parse_instruction(line: str) -> Instruction:
    left, right = line.split(' = ', maxsplit = 1)
    if left == 'mask':
        return UpdateMask(right)
    else:
        mem_pos = MEM_REGEX.fullmatch(left).group(1)
        return UpdateMemory(int(mem_pos), int(right))

def initialize_memory(insts: list[Instruction]) -> dict[int, int]:
    memory = dict[int, int]()
    and_mask = 2 ** 36 - 1
    or_mask = 0

    for inst in insts:
        if isinstance(inst, UpdateMask):
            and_mask = inst.and_mask
            or_mask = inst.or_mask
        elif isinstance(inst, UpdateMemory):
            memory[inst.mem_pos] = inst.value & and_mask | or_mask
        else:
            raise NotImplementedError('Unknown instruction type: ' + inst.__class__.__name__)

    return memory

def gen_memory_positions(base_mem_pos: int, mask: str) -> Iterator[int]:
    base_bits = bin(base_mem_pos)[2:] # take out the 0b prefix
    base_bits = '0' * (len(mask) - len(base_bits)) + base_bits # match mask length
    return map(lambda pos: int(pos, 2), gen_memory_positions_rec(base_bits, mask))

def gen_memory_positions_rec(base: str, mask: str) -> Iterator[str]:
    if mask == '':
        yield ''
    else:
        for pos in gen_memory_positions_rec(base[1:], mask[1:]):
            if mask[0] == 'X':
                yield '0' + pos
                yield '1' + pos
            elif mask[0] == '1':
                yield '1' + pos
            elif mask[0] == '0':
                yield base[0] + pos
            else:
                raise Exception('Unexpected mask value: ' + mask[0])

def initialize_memory_v2(insts: list[Instruction]) -> dict[int, int]:
    memory = dict[int, int]()
    raw_mask = '0' * 26

    for inst in insts:
        if isinstance(inst, UpdateMask):
            raw_mask = inst.raw_mask
        elif isinstance(inst, UpdateMemory):
            for pos in gen_memory_positions(inst.mem_pos, raw_mask):
                memory[pos] = inst.value
        else:
            raise NotImplementedError('Unknown instruction type: ' + inst.__class__.__name__)

    return memory

def solve(input_file: str, skip_part2 = False) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    insts = parse_instructions(full_path)

    start_p1 = time.time_ns()
    memory = initialize_memory(insts)
    print('Part 1 answer:', sum(memory.values()), '(took', time.time_ns() - start_p1, 'ns)')

    if not skip_part2:
        start_p2 = time.time_ns()
        memory_v2 = initialize_memory_v2(insts)
        print('Part 2 answer:', sum(memory_v2.values()), '(took', time.time_ns() - start_p2, 'ns)')
    
    print()

if __name__ == '__main__':
    solve('example.txt', skip_part2 = True) # too slow on part2
    solve('example2.txt')
    solve('input.txt')