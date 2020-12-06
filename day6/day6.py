from itertools import chain
from functools import reduce

def parse_answer_groups(input_file):
    with open(input_file) as f:
        return [
            group.splitlines()
            for group
            in f.read().split('\n\n')]
        
def get_unique_answers(answer_group):
    return set(chain.from_iterable(answer_group))

def get_common_answers(answer_group):
    return reduce(
        lambda ans1, ans2: set(ans1) & set(ans2),
        answer_group)

def solve(input_file):
    print(f'[{input_file}]')
    answer_groups = parse_answer_groups(input_file)
    print('Part 1 answer:', sum([len(get_unique_answers(g)) for g in answer_groups]))
    print('Part 2 answer:', sum([len(get_common_answers(g)) for g in answer_groups]))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')