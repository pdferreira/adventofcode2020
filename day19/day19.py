from __future__ import annotations
from itertools import takewhile
from os import path
from typing import Callable, Optional
from collections.abc import Iterable, Iterator
import time

Parser = Callable[[str], Iterator[str]]

def string(s: str) -> Parser:
    def parse(input: str):
        nonlocal s
        if input.startswith(s):
            yield input[len(s):]

    return parse

def either(parsers: Iterable[Parser]) -> Parser:
    def parse(input: str):
        nonlocal parsers
        for p in parsers:
            yield from p(input) # not handling left-recursion at all

    return parse

def seq(parsers: Iterable[Parser]) -> Parser:
    def parse(input: str):
        nonlocal parsers
        if parsers == []:
            yield input
        else:
            p, *ps = parsers
            for remaining_input in p(input):
                yield from seq(ps)(remaining_input)

    return parse

def rule(i: int, parsers: dict[int, Parser]) -> Parser:
    return lambda input: parsers[i](input)

def parse_input(input_file: str) -> tuple[dict[int, Parser], list[str]]:
    with open(input_file) as f:
        it = iter(f.read().splitlines())
        rules = dict[int, Parser]()
        for line in takewhile(lambda line: line != "", it):
            num, rule = parse_rule(line, rules)
            rules[num] = rule
        messages = list(it)
        return rules, messages

def parse_rule(line: str, rules: dict[int, Parser]) -> tuple[int, Parser]:
    rule_num, _, rule_text = line.partition(': ')

    return int(rule_num), either([
        seq([
            rule(int(atom), rules) if atom.isnumeric() else string(atom.strip('"'))
            for atom
            in alternative.split(' ')
        ])
        for alternative
        in rule_text.split(' | ')
    ])

def match_rule(input: str, rule: Parser) -> bool:
    remaining_input = next(rule(input), None)
    return remaining_input == '' 

def solve(input_file: str, *, expected: tuple[Optional[int], Optional[int]] = (None, None)) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    rules, messages = parse_input(full_path)

    # Part 1
    start_p1 = time.time_ns()
    obtained_p1 = sum(1 for msg in messages if match_rule(msg, rules[0]))

    print('Part 1 answer:', obtained_p1, '(took', time.time_ns() - start_p1, 'ns)')
    if expected[0] is not None and expected[0] != obtained_p1:
        print('Expected:', expected[0])

    # Part 2
    start_p2 = time.time_ns()
    rules[8] = parse_rule('8: 42 | 42 8', rules)[1]
    rules[11] = parse_rule('11: 42 31 | 42 11 31', rules)[1]
    obtained_p2 = sum(1 for msg in messages if match_rule(msg, rules[0]))

    print('Part 2 answer:', obtained_p2, '(took', time.time_ns() - start_p2, 'ns)')
    if expected[1] is not None and expected[1] != obtained_p2:
        print('Expected:', expected[1])

    print()

if __name__ == '__main__':
    solve('example.txt', expected = (2, 2))
    solve('example2.txt', expected = (2, 2))
    solve('example3.txt', expected = (3, 12))
    solve('input.txt', expected = (120, 350))