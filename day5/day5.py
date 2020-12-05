def parse_seat_coords(input_file):
    with open(input_file) as f:
        return [
            parse_seat_coord(coord_code)
            for coord_code
            in f.readlines()]

def parse_seat_coord(coord_code):
    return {
        'row': row_code_to_number(coord_code[:7]),
        'col': col_code_to_number(coord_code[7:])
    }

def row_code_to_number(row_code):
    row_binary = row_code.replace('F', '0').replace('B', '1')
    return int(row_binary, 2)

def col_code_to_number(col_code):
    col_binary = col_code.replace('L', '0').replace('R', '1')
    return int(col_binary, 2)

def calculate_seat_id(seat_coord):
    return seat_coord['row'] * 8 + seat_coord['col']

def max_seat_id(seat_coords):
    return max([calculate_seat_id(c) for c in seat_coords])

def find_empty_seat(seat_coords):
    sorted_seats = sorted([calculate_seat_id(c) for c in seat_coords])
    prev_seat_id = sorted_seats[0]
    for seat_id in sorted_seats[1:]:
        if seat_id - prev_seat_id > 1:
            return seat_id - 1
        else:
            prev_seat_id = seat_id

def solve(input_file):
    print(f'[{input_file}]')
    seat_coords = parse_seat_coords(input_file)
    print('Part 1 answer:', max_seat_id(seat_coords))
    print('Part 2 answer:', find_empty_seat(seat_coords))
    print()

if __name__ == '__main__':
    solve('example.txt')
    solve('input.txt')