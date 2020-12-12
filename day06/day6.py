from itertools import chain
from functools import reduce
from os import path

def parse_answer_groups(input_file: str) -> list[list[str]]:
    with open(input_file) as f:
        return [
            group.splitlines()
            for group
            in f.read().split('\n\n')]
        
def get_unique_answers(answer_group: list[str]) -> set[str]:
    return set(chain.from_iterable(answer_group))

def get_common_answers(answer_group: list[str]) -> set[str]:
    if answer_group == []:
        return set()
    else:
        return reduce(
            lambda ans1, ans2: set(ans1) & set(ans2),
            answer_group[1:],
            set(answer_group[0]))

def solve(input_file: str):
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)
    answer_groups = parse_answer_groups(full_path)
    print('Part 1 answer:', sum([len(get_unique_answers(g)) for g in answer_groups]))
    print('Part 2 answer:', sum([len(get_common_answers(g)) for g in answer_groups]))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')