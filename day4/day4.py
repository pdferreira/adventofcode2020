import re

FIELD_REGEX = re.compile(r'(\w{3}):(\S+)')
HEIGHT_REGEX = re.compile(r'(\d+)(cm|in)')
COLOR_REGEX = re.compile(r'#[0-9a-f]{6}')
PASSPORT_ID_REGEX = re.compile(r'\d{9}')

MANDATORY_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
EYE_COLORS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

def parse_passports(input_file):
    with open(input_file) as f:
        return [
            passport_text
            for passport_text
            in f.read().split('\n\n')]

def parse_fields(passport_text):
    return dict(FIELD_REGEX.findall(passport_text))

def validate_year(year_text, min, max):
    try:
        return min <= int(year_text) <= max
    except ValueError:
        return False

def validate_height(height_text):
    height_match = HEIGHT_REGEX.fullmatch(height_text)
    if height_match:
        height = int(height_match.group(1))
        unit = height_match.group(2)
        if unit == 'cm':
            return 150 <= height <= 193
        elif unit == 'in':
            return 59 <= height <= 76

    return False

def validate_color(color_text):
    return COLOR_REGEX.fullmatch(color_text) is not None

def validate_eye_color(color_text):
    return color_text in EYE_COLORS

def validate_passport_id(id_text):
    return PASSPORT_ID_REGEX.fullmatch(id_text) is not None

def is_valid_passport(passport_text, deep_validation):
    pp_fields = parse_fields(passport_text)

    if not MANDATORY_FIELDS <= set(pp_fields):
        return False

    if deep_validation:
        return all([
            validate_year(pp_fields['byr'], 1920, 2002),
            validate_year(pp_fields['iyr'], 2010, 2020),
            validate_year(pp_fields['eyr'], 2020, 2030),
            validate_height(pp_fields['hgt']),
            validate_color(pp_fields['hcl']),
            validate_eye_color(pp_fields['ecl']),
            validate_passport_id(pp_fields['pid'])
        ])

    return True

def count_valid_passports(passport_texts, deep_validation):
    return len([
        pp_text
        for pp_text
        in passport_texts
        if is_valid_passport(pp_text, deep_validation)
    ])

def solve(input_file):
    print(f'[{input_file}]')
    passport_texts = parse_passports(input_file)
    print('Part 1 answer:', count_valid_passports(passport_texts, deep_validation = False))
    print('Part 2 answer:', count_valid_passports(passport_texts, deep_validation = True))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('example2_invalid.txt')
    solve('example2_valid.txt')
    solve('input.txt')