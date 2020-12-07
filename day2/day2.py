from os import path
from typing import Callable

Policy = tuple[int, int, str, str]

def parse_policy(input_line: str) -> Policy:
    (policy, _, password) = input_line.partition(': ')
    (prange, _, pletter) = policy.partition(' ')
    (a, _, b) = prange.partition('-')
    return (int(a), int(b), pletter, password)


def parse_file(input_file: str) -> list[Policy]:
    full_path = path.join(path.dirname(__file__), input_file)
    with open(full_path) as f:
        return [parse_policy(line) for line in f.readlines()]
        
def validate_policy_part1(minOccur: int, maxOccur: int, letter: str, password: str) -> bool:
    return minOccur <= password.count(letter) <= maxOccur

def validate_policy_part2(fstPos: int, sndPos: int, letter: str, password: str) -> bool:
    fstMatches = password[fstPos - 1] == letter
    sndMatches = password[sndPos - 1] == letter
    return fstMatches != sndMatches

def solve(password_policies: list[Policy], validation_fn: Callable) -> int:
    return [
        validation_fn(a, b, letter, password)
        for (a, b, letter, password)
        in password_policies].count(True)
  
if __name__ == '__main__':
    pwd_policies = parse_file('input.txt')
    print('Part 1 answer:', solve(pwd_policies, validate_policy_part1))
    print('Part 2 answer:', solve(pwd_policies, validate_policy_part2))