from functools import reduce
import re

BAG_REGEX = re.compile(r'(\d+) (\w+ \w+) bags?')

SubBag = tuple[int, str]
Rule = tuple[str, list[SubBag]]

def parse_rules(input_file: str) -> list[Rule]:
    with open(input_file) as f:
        return [
            parse_rule(rule_text)
            for rule_text
            in f.read().splitlines()]

def parse_rule(rule_text: str) -> Rule:
    bag_type, rest = rule_text.split(' bags contain ', maxsplit=1)
    if rest == 'no other bags.':
        return bag_type, []
    else:
        inner_bags = rest.rstrip('.').split(', ')
        return bag_type, [parse_bag(b) for b in inner_bags]

def parse_bag(bag_text: str) -> SubBag:
    match = BAG_REGEX.fullmatch(bag_text)
    if match is not None:
        return int(match.group(1)), match.group(2)

def create_inverted_rule_map(rules: list[Rule]) -> dict[str, set[str]]:
    irule_map = dict()
    for bag_type, sub_bags in rules:
        for _, b in sub_bags:
            if b not in irule_map:
                irule_map[b] = { bag_type }
            else:
                irule_map[b].add(bag_type)
    
    return irule_map

def get_super_bags_of(bag_type: str, irule_map: dict[str, set[str]]) -> set[str]:
    if bag_type in irule_map:
        super_bags = irule_map[bag_type]
        return super_bags | reduce(lambda acc, b: acc | get_super_bags_of(b, irule_map), super_bags, set())
    else:
        return set()

def count_sub_bags_of(bag_type: str, rule_map: dict[str, list[SubBag]]) -> int:
    if bag_type in rule_map:
        return sum([
            n_rep + n_rep * count_sub_bags_of(sub_bag_type, rule_map)
            for n_rep, sub_bag_type
            in rule_map[bag_type]
        ])
    else:
        return 0

def solve(input_file: str) -> None:
    print(f'[{input_file}]')
    rules = parse_rules(input_file)
    rule_map = dict(rules)
    irule_map = create_inverted_rule_map(rules)
    print('Part 1 answer:', len(get_super_bags_of('shiny gold', irule_map)))
    print('Part 2 answer:', count_sub_bags_of('shiny gold', rule_map))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('example2.txt')
    solve('input.txt')