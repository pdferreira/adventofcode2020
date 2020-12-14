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
    and_mask = 1 << 36 - 1
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

def gen_memory_positions(base: int, mask: str) -> Iterator[int]:
    '''
    Generate memory positions by applying the `mask` to `base` by recursively building bit-strings.
    '''
    base_bits = bin(base)[2:] # take out the 0b prefix
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


def gen_memory_positions_v2(base: int, mask: str, mask_idx: int = 0) -> Iterator[int]:
    '''
    Generate memory positions by applying the `mask` to `base` as a series of bitwise operations.
    Not actually faster than v1.
    '''
    mask_len = len(mask)
    if mask_idx >= mask_len:
        yield base
    else:
        one_mask = 1 << (mask_len - 1 - mask_idx) # mask with 1 at the current bit else 0s
        if mask[mask_idx] == 'X':
            zero_mask = ((1 << mask_len) - 1) ^ one_mask # mask with 0 at the current bit else 1s
            yield from gen_memory_positions_v2(base & zero_mask, mask, mask_idx + 1)
            yield from gen_memory_positions_v2(base | one_mask, mask, mask_idx + 1)
        elif mask[mask_idx] == '1':
            yield from gen_memory_positions_v2(base | one_mask, mask, mask_idx + 1)
        elif mask[mask_idx] == '0':
            yield from gen_memory_positions_v2(base, mask, mask_idx + 1)
        else:
            raise Exception('Unexpected mask vlue: ' + mask[mask_idx])


def initialize_memory_v2(insts: list[Instruction]) -> dict[int, int]:
    memory = dict[int, int]()
    raw_mask = '0' * 26

    for inst in insts:
        if isinstance(inst, UpdateMask):
            raw_mask = inst.raw_mask
        elif isinstance(inst, UpdateMemory):
            for pos in gen_memory_positions_v2(inst.mem_pos, raw_mask):
                memory[pos] = inst.value
        else:
            raise NotImplementedError('Unknown instruction type: ' + inst.__class__.__name__)

    return memory

def optimize_instructions(insts: list[Instruction], *, within_masks_only: bool) -> list[Instruction]:
    '''
    Eliminates repeated writes to the same memory location, preserving the last one.
    If `within_masks_only` is True, preserves the last one for each mask.
    '''
    return optimize_instructions_rec(insts, within_masks_only, set())

def optimize_instructions_rec(insts: list[Instruction], within_masks_only: bool, written_mem_pos: set[int]) -> list[Instruction]:
    if insts == []:
        return []
    else:
        *rest, last = insts
        if isinstance(last, UpdateMask):
            if within_masks_only:
                written_mem_pos = set()
            
            optimized_rest = optimize_instructions_rec(rest, within_masks_only, written_mem_pos)
            optimized_rest.append(last)
            return optimized_rest

        elif isinstance(last, UpdateMemory):
            if last.mem_pos in written_mem_pos:
                return optimize_instructions_rec(rest, within_masks_only, written_mem_pos)
            else:
                written_mem_pos.add(last.mem_pos)
                optimized_rest = optimize_instructions_rec(rest, within_masks_only, written_mem_pos)
                optimized_rest.append(last)
                return optimized_rest
        
        else:
            raise NotImplementedError('Unknown instruction type: ' + last.__class__.__name__)

def solve(input_file: str, *, optimize = True, skip_part2 = False) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    insts = parse_instructions(full_path)

    start_p1 = time.time_ns()
    insts_p1 = optimize_instructions(insts, within_masks_only = False) if optimize else insts
    memory = initialize_memory(insts_p1)
    print('Part 1 answer:', sum(memory.values()), '(took', time.time_ns() - start_p1, 'ns)')

    if not skip_part2:
        start_p2 = time.time_ns()
        insts_p2 = optimize_instructions(insts, within_masks_only = True) if optimize else insts
        memory_v2 = initialize_memory_v2(insts_p2)
        print('Part 2 answer:', sum(memory_v2.values()), '(took', time.time_ns() - start_p2, 'ns)')
    
    print()

if __name__ == '__main__':
    solve('example.txt', skip_part2 = True) # too slow on part2
    solve('example2.txt')
    solve('input.txt', optimize = False)