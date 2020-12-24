from __future__ import annotations
from functools import reduce
from typing import Optional, cast
import time

class Node:
    value: int
    next: Node | None
    prev: Node | None

    def __init__(self, value: int):
        self.value = value

    def link(self, other: Node) -> Node:
        self.next = other
        other.prev = self
        return other

class NodeRange:
    value_range: range
    next: NodeRange | None
    prev: NodeRange | None

    def __init__(self, value_range: int | range):
        if isinstance(value_range, int):
            value_range = range(value_range, value_range + 1)

        self.value_range = value_range

    def link(self, other: NodeRange, try_to_merge: bool = False) -> NodeRange:
        if try_to_merge and self.value_range.stop == other.value_range.start:
            self.value_range = range(self.value_range.start, other.value_range.stop)
            self.next = other.next
            other.next = None
            other.prev = None
            return self
        else:
            self.next = other
            other.prev = self
            return other

    def split_at(self, value: int) -> NodeRange:
        assert value <= self.value_range.stop
        if value == self.value_range.stop:
            return self
            
        other = NodeRange(range(value, self.value_range.stop))
        self.value_range = range(self.value_range.start, value)
        
        if self.next:
            other.link(self.next)
        
        self.link(other)
        return other

    def size(self) -> int:
        return len(self.value_range)

def play(labeling: list[int], n_moves: int) -> list[int]:
    if n_moves == 0:
        return labeling

    curr, *rest = labeling
    picked = rest[0:3]
    dest = curr - 1
    (rel_dest_idx, _), *_ = sorted(enumerate(rest[3:]), key = lambda elem: (dest - elem[1]) % 9)
    dest_idx = 3 + rel_dest_idx + 1 # 3 picked and 1 after
    return play(rest[3:dest_idx] + picked + rest[dest_idx:] + [curr], n_moves = n_moves - 1)

def labeling_to_str(labeling: list[int], pivot = 1) -> str:
    idx_of_pivot = labeling.index(pivot)
    labeling_from_pivot = labeling[idx_of_pivot + 1:] + labeling[:idx_of_pivot]
    return ''.join(map(str, labeling_from_pivot))
    
'''
..., 999998, 999999, 1000000, (3), 8, 9, 1, 2, 5, 4, 6, 7, 10, 11, 12, 13, ...
..., 999998, 999999, 1000000, 3, (2), 8, 9, 1, 5, 4, 6, 7, 10, 11, 12, 13, ...
..., 999998, 999999, 1000000, 8, 9, 1, 3, 2, (5), 4, 6, 7, 10, 11, 12, 13, ...
..., 999998, 999999, 1000000, 8, 9, 1, 3, 4, 6, 7, 2, 5, (10), 11, 12, 13, ...
..., 999998, 999999, 1000000, 8, 9, 11, 12, 13, 1, 3, 4, 6, 7, 2, 5, 10, (14), 15, 16, 17, ...
..., 999998, 999999, 1000000, 8, 9, 11, 12, 13, 15, 16, 17, 1, 3, 4, 6, 7, 2, 5, 10, 14, (18), ...
..., 999998, 999999, 1000000, 8, 9, 11, 12, 13, 15, 16, 17, 19, 20, 21, 1, 3, 4, 6, 7, 2, 5, 10, 14, 18, (22) ...
...
..., (999998), 999999, 1000000, 8, 9, 11, 12, 13, ..., 999997, 1, 3, 4, 6, 7, 2, 5, 10, 14, 18, 22, ...
..., 999998, (9), 11, 12, 13, ..., 999997, 999999, 1000000, 8, 1, 3, 4, 6, 7, 2, 5, 10, 14, 18, 22, ...
..., 999998, 9, (15), 16, 17, ..., 999997, 999999, 1000000, 8, 11, 12, 13, 1, 3, 4, 6, 7, 2, 5, 10, 14, 18, 22, ...
..., 999998, 9, 15, (20), ..., 999997, 999999, 1000000, 8, 11, 12, 13, 1, 3, 4, 6, 7, 2, 5, 10, 14, 16, 17, 19, 18, 22, ...
'''

def play_v2(labeling_start: list[int], n_moves: int) -> list[int]:
    max_value = 1000000
    labeling = labeling_start + list(range(max(labeling_start) + 1, max_value + 1))
    while n_moves > 0:
        curr, *rest = labeling
        picked = rest[0:3]
        dest = curr - 1
        while dest in picked:
            dest -= 1

        if dest < 1:
            dest = max_value

        # print('Move:', n_moves, 'Curr:', curr, 'Picked:', picked, 'Dest:', dest)
        dest_idx = rest.index(dest)
        labeling = rest[3:(dest_idx + 1)] + picked + rest[(dest_idx + 1):] + [curr]
        n_moves -= 1
    
    return labeling

def play_v3(labeling_start: list[int], n_moves: int) -> list[int]:
    max_value = 1000000
    labeling = labeling_start + list(range(max(labeling_start) + 1, max_value + 1))
    labeling_len = len(labeling)
    
    def get_num_at(idx: int) -> int:
        nonlocal labeling, labeling_len
        return labeling[idx % labeling_len]

    def set_num_at(idx: int, num: int):
        nonlocal labeling, labeling_len
        labeling[idx % labeling_len] = num

    curr_idx = 0
    max_value_idx = labeling_len - 1
    while n_moves > 0:
        curr = labeling[curr_idx]
        picked = [get_num_at(curr_idx + i + 1) for i in range(3)]
        dest = curr - 1

        while dest in picked:
            dest -= 1

        if dest < 1:
            dest = max_value
            # assert labeling[-1] == max_value

        dest_idx = labeling.index(dest)
        if abs(dest_idx - curr_idx) > labeling_len / 2:
            shift_idx = curr_idx
            while shift_idx != dest_idx:
                set_num_at(shift_idx + 3, get_num_at(shift_idx))
                shift_idx = (shift_idx - 1) % labeling_len

            shift_idx += 1
            curr_idx += 3
        else:
            shift_idx = curr_idx + 1
            while get_num_at(shift_idx - 1) != dest:
                set_num_at(shift_idx, get_num_at(shift_idx + 3))
                shift_idx += 1

        for i in range(3):
            set_num_at(shift_idx + i, picked[i])

        curr_idx = (curr_idx + 1) % len(labeling)
        n_moves -= 1
    
    return labeling

def play_v4(labeling_start: list[int], n_moves: int) -> list[int]:
    max_value = 1000000

    # Build list
    head = Node(0) # dummy node
    last = reduce(lambda prev, num: prev.link(Node(num)), labeling_start, head)
    head = head.next
    last = reduce(lambda prev, num: prev.link(Node(num)), range(max(labeling_start) + 1, max_value + 1), last)

    # Make it circular
    last.link(cast(Node, head))

    curr_node = head
    while n_moves > 0:
        curr = curr_node.value
        
        # Get the picked items head and last nodes
        picked_head = curr_node.next
        picked_last = picked_head.next.next
        picked = [picked_head.value, picked_head.next.value, picked_last.value]

        # Find the destination node
        dest = curr - 1
        while dest in picked:
            dest -= 1

        if dest < 1:
            dest = max_value

        # print('Move:', n_moves, 'Curr:', curr, 'Picked:', picked, 'Dest:', dest)
        dest_node = picked_last.next
        while dest_node.value != dest:
            dest_node = dest_node.next

        # Move the picked sub-list to after the dest node
        after_dest_node = dest_node.next
        after_picked_nodes = picked_last.next

        dest_node.link(cast(Node, picked_head))
        picked_last.link(cast(Node, after_dest_node))
        curr_node.link(cast(Node, after_picked_nodes))

        # Advance the current
        curr_node = curr_node.next
        n_moves -= 1
    
    # Convert to list
    labeling = list[int]()
    labeling.append(head.value)
    curr_node = head.next
    while curr_node != head:
        labeling.append(curr_node.value)
        curr_node = curr_node.next

    return labeling

def play_v5(labeling_start: list[int], n_moves: int) -> list[int]:
    max_value = 1000000

    # Build list
    head = NodeRange(range(0)) # dummy node
    last = reduce(lambda prev, num: prev.link(NodeRange(num)), labeling_start, head)
    head = head.next
    last = last.link(NodeRange(range(max(labeling_start) + 1, max_value + 1)))

    # Make it circular
    last.link(cast(NodeRange, head))

    start_t = time.time_ns()
    curr_node = head
    curr_node_i = 0
    while n_moves > 0:
        if n_moves % 100000 == 0:
            end_t = time.time_ns()
            print('Missing moves:', n_moves, 'Ellapsed:', end_t - start_t, 'ns')
            start_t = end_t

        curr = curr_node.value_range.start + curr_node_i
        
        # Get the picked items head and last nodes
        if curr_node.size() > 1:
            picked_head = curr_node.split_at(curr + 1)
            picked_last = picked_head
            if picked_head.size() > 3:
                picked_head.split_at(curr + 4)
        else:
            picked_head = curr_node.next
            picked_last = picked_head
            
        missing_picks = 3 - picked_head.size()
        while missing_picks > 0:
            picked_last = picked_last.next
            missing_picks -= picked_last.size()

        if missing_picks < 0:
            picked_last.split_at(picked_last.value_range.stop + missing_picks)

        picked = list[int]()
        curr_picked_node = picked_head
        while curr_picked_node != picked_last.next:
            picked.extend(curr_picked_node.value_range)
            curr_picked_node = curr_picked_node.next

        # Find the destination node
        dest = curr - 1
        while dest in picked:
            dest -= 1

        if dest < 1:
            dest = max_value

        # print('Move:', n_moves, 'Curr:', curr, 'Picked:', picked, 'Dest:', dest)
        dest_node = picked_last.next
        while dest not in dest_node.value_range:
            dest_node = dest_node.next

        # Move the picked sub-list to after the dest node
        if dest_node.size() > 1:
            dest_node.split_at(dest + 1)
            
        after_dest_node = dest_node.next
        after_picked_nodes = picked_last.next

        dest_node.link(cast(NodeRange, picked_head), try_to_merge = True)
        picked_last.link(cast(NodeRange, after_dest_node), try_to_merge = True)
        curr_node.link(cast(NodeRange, after_picked_nodes), try_to_merge = True)

        # Advance the current
        curr_node_i += 1
        if curr_node_i == curr_node.size():
            curr_node_i = 0
            curr_node = curr_node.next
        n_moves -= 1
    
    # Convert to list
    labeling = list[int]()
    labeling.extend(curr_node.value_range)
    last = curr_node.prev
    curr_node = curr_node.next
    while curr_node != last:
        labeling.extend(curr_node.value_range)
        curr_node = curr_node.next

    return labeling
    
def solve(labeling_str: str, *, expected: tuple[Optional[str], Optional[str]] = (None, None)) -> None:
    print(f'[{labeling_str}]')

    # Common
    start_common = time.time_ns()
    labeling = [int(c) for c in labeling_str]
    time_common = time.time_ns() - start_common

    # Part 1
    start_p1 = time.time_ns()
    new_labeling = play(labeling, n_moves = 100)
    obtained_p1 = labeling_to_str(new_labeling)
    time_p1 = (time.time_ns() - start_p1) + time_common

    print('Part 1 answer:', obtained_p1, '(took', time_p1, 'ns)')
    if expected[0] is not None and expected[0] != obtained_p1:
        print('Expected:', expected[0])

    # Part 2
    start_p2 = time.time_ns()
    new_labeling_v2 = play_v5(labeling, n_moves = 10000000)
    idx_of_1 = new_labeling_v2.index(1)
    a, b = new_labeling_v2[(idx_of_1 + 1) % len(new_labeling_v2)], new_labeling_v2[(idx_of_1 + 2) % len(new_labeling_v2)]
    print(a, b)
    obtained_p2 = a * b
    time_p2 = (time.time_ns() - start_p2) + time_common

    print('Part 2 answer:', obtained_p2, '(took', time_p2, 'ns)')
    if expected[1] is not None and expected[1] != obtained_p2:
        print('Expected:', expected[1])

    print()

if __name__ == '__main__':
    solve('389125467', expected = ('67384529', None))
    solve('963275481', expected = (None, None))