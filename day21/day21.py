from __future__ import annotations
from os import path
from itertools import chain
from typing import Optional
from dataclasses import dataclass
import time
import re

@dataclass
class Food:
    ingredients: set[str]
    allergens: set[str]

    FOOD_PATTERN = re.compile(r'(?P<ingredients>\w+( \w+)*) \(contains (?P<allergens>\w+(, \w+)*)\)')
    
    @staticmethod
    def parse(line: str) -> Food:
        match = Food.FOOD_PATTERN.fullmatch(line)
        if match:
            ingredients = set(match.group('ingredients').split(' '))
            allergens = set(match.group('allergens').split(', '))
            return Food(ingredients, allergens)
        else:
            raise Exception('Unable to match against line: ' + line)

def parse_foods(input_file: str) -> list[Food]:
    with open(input_file) as f:
        return [
            Food.parse(line)
            for line
            in f.read().splitlines()]

def propagate_ingredient_uniqueness(source_allergen: str, allergen_map: dict[str, set[str]]):
    allergens_to_check = [source_allergen]
    while allergens_to_check:
        allergen = allergens_to_check.pop(0)
        possible_ings = allergen_map[allergen]
        if len(possible_ings) == 1:
            ing = list(possible_ings)[0]
            for other_allergen in allergen_map:
                if other_allergen != allergen:
                    other_possible_ings = allergen_map[other_allergen]
                    if ing in other_possible_ings:
                        other_possible_ings.remove(ing)
                        allergens_to_check.append(other_allergen)

def map_allergens_to_ingredients(foods: list[Food]) -> dict[str, set[str]]:
    allergen_to_ingredient = dict[str, set[str]]()
    for f in foods:
        for allergen in f.allergens:
            if allergen not in allergen_to_ingredient:
                allergen_to_ingredient[allergen] = f.ingredients.copy()
                propagate_ingredient_uniqueness(allergen, allergen_to_ingredient)
            else:
                possible_ings = allergen_to_ingredient[allergen]
                if len(possible_ings) > 1:
                    impossible_ings = possible_ings - f.ingredients
                    if impossible_ings:
                        for ing in impossible_ings: 
                            possible_ings.remove(ing)
                        
                        propagate_ingredient_uniqueness(allergen, allergen_to_ingredient)              

    return allergen_to_ingredient

def solve(input_file: str, *, expected: tuple[Optional[int], Optional[str]] = (None, None)) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    foods = parse_foods(full_path)
    print(foods)

    allergen_map = map_allergens_to_ingredients(foods)
    print(allergen_map)

    ingredients_with_allergens = set(chain(*allergen_map.values()))

    # Part 1
    start_p1 = time.time_ns()
    obtained_p1 = sum(len(f.ingredients - ingredients_with_allergens) for f in foods)

    print('Part 1 answer:', obtained_p1, '(took', time.time_ns() - start_p1, 'ns)')
    if expected[0] is not None and expected[0] != obtained_p1:
        print('Expected:', expected[0])

    # Part 2
    start_p2 = time.time_ns()
    obtained_p2 = ','.join(list(allergen_map[allergen])[0] for allergen in sorted(allergen_map.keys()))

    print('Part 2 answer:', obtained_p2, '(took', time.time_ns() - start_p2, 'ns)')
    if expected[1] is not None and expected[1] != obtained_p2:
        print('Expected:', expected[1])

    print()

if __name__ == '__main__':
    solve('example.txt', expected = (5, 'mxmxvkd,sqjhc,fvjkl'))
    solve('input.txt', expected = (2584, 'fqhpsl,zxncg,clzpsl,zbbnj,jkgbvlxh,dzqc,ppj,glzb'))