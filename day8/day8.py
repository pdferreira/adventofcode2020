from os import path
from typing import Optional, cast
from enum import Enum

class Operator(Enum):
    NOP = 'nop'
    ACC = 'acc'
    JMP = 'jmp'

Instruction = tuple[Operator, int]

def parse_instructions(input_file: str) -> list[Instruction]:
    with open(input_file) as f:
        return [
            parse_instruction(instruction_text)
            for instruction_text
            in f.read().splitlines()]

def parse_instruction(instruction_text: str) -> Instruction:
    op, value = instruction_text.split(' ', maxsplit = 1)
    return Operator(op), int(value)

def run_until_loop(insts: list[Instruction]) -> tuple[int, bool]:
    acc = 0
    pc = 0
    visited = set[int]()
    while pc < len(insts):
        if pc in visited:
            return acc, True
        else:
            visited.add(pc)

        op, value = insts[pc]
        if op == Operator.NOP:
            pc += 1
            pass
        elif op == Operator.ACC:
            acc += value
            pc += 1
        elif op == Operator.JMP:
            pc += value
        else:
            raise Exception('Unknown instruction: ' + op)

    return acc, False

def run_until_fixed(insts: list[Instruction]) -> Optional[tuple[int, list[Instruction]]]:
    for idx, inst in enumerate(insts):
        op, value = inst
        
        if op == Operator.NOP:
            fixed_op = cast(Operator, Operator.JMP) # Pyright keeps inferring as Literal and messing things up
        elif op == Operator.JMP:
            fixed_op = cast(Operator, Operator.NOP)
        else:
            continue

        fixed_insts = insts[:idx] + [(fixed_op, value)] + insts[(idx + 1):]
        acc, hit_loop = run_until_loop(fixed_insts)
        if not hit_loop:
            return acc, fixed_insts
       
def solve(input_file: str) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)
    insts = parse_instructions(full_path)
    print('Part 1 answer:', run_until_loop(insts)[0])
    print('Part 2 answer:', run_until_fixed(insts)[0])
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')