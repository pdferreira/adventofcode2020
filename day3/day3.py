from functools import reduce

def parse_file(input_file):
    with open(input_file) as f:
        return f.read().splitlines()
        
def is_tree(tile):
    return tile == '#'

def count_trees_on_slope(travel_map, dx, dy, x=0, y=0):
    if travel_map == []:
        return 0

    map_top = travel_map[0]
    top_trees = 1 if is_tree(map_top[x]) else 0

    new_x = (x + dx) % len(map_top)
    rest_trees = count_trees_on_slope(travel_map[dy:], dx, dy, new_x, y + dy)
    
    return top_trees + rest_trees

def multiply_tree_counts(travel_map, slopes):
    tree_counts = [count_trees_on_slope(travel_map, dx, dy) for dx, dy in slopes]
    return reduce(lambda a, b: a * b, tree_counts)

if __name__ == '__main__':
    travel_map = parse_file('input.txt')
    print('Part 1 answer:', count_trees_on_slope(travel_map, 3, 1))
    print('Part 2 answer:', multiply_tree_counts(travel_map, [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]))