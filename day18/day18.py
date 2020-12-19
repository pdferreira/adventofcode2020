from __future__ import annotations
from os import path
from typing import Optional
import time
import re

TOKEN_PATTERN = re.compile(r'\d+|[+*()]|\s+')

def parse_expressions(input_file: str) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()

def tokenize(expr_str: str) -> list[str]:
    return [t for t in TOKEN_PATTERN.findall(expr_str) if not t.isspace()]

def evaluate(expr_str: str) -> int:
    tokens = tokenize('(' + expr_str + ')')

    v, ts, num_parens = evaluate_rec(tokens)
    assert ts == []
    assert num_parens == 0
    return v

def evaluate_p2(expr_str: str) -> int:
    tokens = tokenize('(' + expr_str + ')')

    v, ts, num_parens = evaluate_rec_v2(tokens)
    assert ts == []
    assert num_parens == 0
    return v

def evaluate_rec(tokens: list[str], num_parens: int = 0, acc_value: Optional[int] = None) -> tuple[int, list[str], int]:
    # print(tokens, num_parens, acc_value)
    if tokens == []:
        assert acc_value is not None
        assert num_parens == 0
        return acc_value, [], 0

    t, *ts = tokens
    if t.isnumeric():
        return int(t), ts, num_parens
    elif t == '+':
        assert acc_value is not None
        v, next_ts, _ = evaluate_rec(ts, num_parens)
        return acc_value + v, next_ts, num_parens
    elif t == '*':
        assert acc_value is not None
        v, next_ts, _ = evaluate_rec(ts, num_parens)
        return acc_value * v, next_ts, num_parens
    elif t == '(':
        v, next_ts, remaining_parens = evaluate_rec(ts, num_parens + 1)
        while remaining_parens > num_parens:
            v, next_ts, remaining_parens = evaluate_rec(next_ts, remaining_parens, v)
        
        return v, next_ts, remaining_parens
    elif t == ')':
        assert acc_value is not None
        return acc_value, ts, num_parens - 1
    else:
        raise NotImplementedError()

def evaluate_rec_v2(tokens: list[str], num_parens: int = 0, acc_value: Optional[int] = None) -> tuple[int, list[str], int]:
    # print(tokens, num_parens, acc_value)
    if tokens == []:
        assert acc_value is not None
        assert num_parens == 0
        return acc_value, [], 0

    t, *ts = tokens
    if t.isnumeric():
        return int(t), ts, num_parens
    elif t == '+':
        assert acc_value is not None
        v, next_ts, remaining_parens = evaluate_rec_v2(ts, num_parens)
        return acc_value + v, next_ts, remaining_parens
    elif t == '*':
        assert acc_value is not None
        v, next_ts, remaining_parens = evaluate_rec_v2(ts, num_parens)
        
        # delay multiplication until every sum and number is consumed
        while next_ts and next_ts[0] not in ['*', ')']:
            v, next_ts, remaining_parens = evaluate_rec_v2(next_ts, remaining_parens, v)
        
        return acc_value * v, next_ts, remaining_parens
    elif t == '(':
        v, next_ts, remaining_parens = evaluate_rec_v2(ts, num_parens + 1)

        # eval until the matching parens is found
        while remaining_parens > num_parens:
            v, next_ts, remaining_parens = evaluate_rec_v2(next_ts, remaining_parens, v)
        
        return v, next_ts, remaining_parens
    elif t == ')':
        assert acc_value is not None
        return acc_value, ts, num_parens - 1
    else:
        raise NotImplementedError()

def solve(input_file: str, *, expected: tuple[Optional[int], Optional[int]] = (None, None)) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    exprs = parse_expressions(full_path)

    # Part 1
    start_p1 = time.time_ns()
    # for e in exprs:
    #     print(e, '=', evaluate(e))

    obtained_p1 = sum(map(evaluate, exprs))

    print('Part 1 answer:', obtained_p1, '(took', time.time_ns() - start_p1, 'ns)')
    if expected[0] is not None and expected[0] != obtained_p1:
        print('Expected:', expected[0])

    # Part 2
    start_p2 = time.time_ns()
    # for e in exprs:
    #     print(e, '=', evaluate_p2(e))

    obtained_p2 = sum(map(evaluate_p2, exprs))

    print('Part 2 answer:', obtained_p2, '(took', time.time_ns() - start_p2, 'ns)')
    if expected[1] is not None and expected[1] != obtained_p2:
        print('Expected:', expected[1])

    print()

if __name__ == '__main__':
    solve('example.txt', expected = (26457, 694173))
    solve('input.txt', expected = (650217205854, 20394514442037))