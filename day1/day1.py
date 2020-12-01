def find_pair(num_array, expected_sum):
    expected_nums = set()
    for num in num_array:
        if num in expected_nums:
            return (num, expected_sum - num)
        else:
            expected_nums.add(expected_sum - num)

def solve_part1(num_array, expected_sum):
    (a, b) = find_pair(num_array, expected_sum)
    return a * b

def read_file(input_file):
    with open(input_file) as f:
        return [int(line) for line in f.readlines()]

def find_triple(num_array, expected_sum):
    for num in num_array:
        pair = find_pair(num_array[1:], expected_sum - num)
        if pair != None:
            return (num,) + pair

def solve_part2(num_array, expected_sum):
    (a, b, c) = find_triple(num_array, expected_sum)
    return a * b * c

if __name__ == '__main__':
    num_array = read_file('input.txt')
    print('Part 1 answer:', solve_part1(num_array, 2020))
    print('Part 2 answer:', solve_part2(num_array, 2020))