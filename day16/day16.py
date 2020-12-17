from __future__ import annotations
from os import path
from typing import Optional
from itertools import chain
from functools import reduce
import re
import time

Ticket = list[int]

class Field:
    PATTERN = re.compile(r'([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)')

    def __init__(self, name: str, lower_range: range, upper_range: range):
        self.name = name
        self.lower_range = lower_range
        self.upper_range = upper_range

    def validate(self, value: int) -> bool:
        return value in self.lower_range or value in self.upper_range

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def parse(field_str: str) -> Field:
        match = Field.PATTERN.fullmatch(field_str)
        if match is None:
            raise Exception('Invalid field: ' + field_str)
        else:
            name, lower_min, lower_max, upper_min, upper_max = match.groups()
            lower_range = range(int(lower_min), int(lower_max) + 1)
            upper_range = range(int(upper_min), int(upper_max) + 1)
            return Field(name, lower_range, upper_range)

def parse_notes(input_file: str) -> tuple[list[Field], Ticket, list[Ticket]]:
    with open(input_file) as f:
        fields_str, my_ticket_str, nearby_tickets_str = f.read().split('\n\n', maxsplit = 2)

        fields = [Field.parse(line) for line in fields_str.splitlines()]
        my_ticket = parse_ticket(my_ticket_str.splitlines()[1])
        nearby_tickets = [parse_ticket(line) for line in nearby_tickets_str.splitlines()[1:]]
        return fields, my_ticket, nearby_tickets

def parse_ticket(ticket_str: str) -> Ticket:
    return [int(v) for v in ticket_str.split(',')]

def is_valid_ticket(fields: list[Field], ticket: Ticket) -> bool:
    return all(
        any(f.validate(value) for f in fields)
        for value
        in ticket
    )

def scanning_error_rate(fields: list[Field], tickets: list[Ticket]) -> int:
    return sum(
        value
        for value
        in chain(*tickets)
        if not any(f.validate(value) for f in fields)
    )

def get_fields_in_ticket_order(fields: list[Field], tickets: list[Ticket]) -> list[Field]:
    valid_tickets = [t for t in tickets if is_valid_ticket(fields, t)]
    total_fields = len(fields)
    possible_positions = dict((f, set(range(total_fields))) for f in fields)

    # identify what are the impossible positions for a field, based on the real values
    for f in fields:
        for i in range(total_fields):
            if any(not f.validate(t[i]) for t in valid_tickets):
                possible_positions[f].remove(i)

    # try to assign each field one position, starting by those with 1 option
    sorted_by_possibilities = sorted(possible_positions.items(), key = lambda item: len(item[1]))
    final_positions = dict[Field, int]()

    while sorted_by_possibilities:
        f, idxs = sorted_by_possibilities.pop(0)
        [i] = idxs  # assuming a single position at this point
        final_positions[f] = i

        # remove index from the others' possibilities
        for _, other_idxs in sorted_by_possibilities:
            other_idxs.discard(i)

        # re-sort based on the number of possibilies
        sorted_by_possibilities.sort(key = lambda item: len(item[1]))
                
    # finally sort the fields by the found positions
    return sorted(fields, key = lambda f: final_positions[f])

def solve(input_file: str, *, expected: tuple[Optional[int], Optional[int]] = (None, None)) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    fields, my_ticket, nearby_tickets = parse_notes(full_path)

    # Part 1
    start_p1 = time.time_ns()
    obtained_p1 = scanning_error_rate(fields, nearby_tickets)
    
    print('Part 1 answer:', obtained_p1, '(took', time.time_ns() - start_p1, 'ns)')
    if expected[0] is not None and expected[0] != obtained_p1:
        print('Expected:', expected[0])

    # Part 2
    start_p2 = time.time_ns()
    ordered_fields = get_fields_in_ticket_order(fields, [my_ticket] + nearby_tickets)
    print('Ordered fields:', [str(f) for f in ordered_fields])

    departure_values = (v for f, v in zip(ordered_fields, my_ticket) if f.name.startswith('departure'))
    obtained_p2 = reduce(lambda acc, v: acc * v, departure_values, 1)

    print('Part 2 answer:', obtained_p2, '(took', time.time_ns() - start_p2, 'ns)')
    if expected[1] is not None and expected[1] != obtained_p2:
        print('Expected:', expected[1])

    print()

if __name__ == '__main__':
    solve('example.txt', expected = (71, None))
    solve('input.txt', expected = (19240, 21095351239483))