from __future__ import annotations
from functools import reduce
from os import path
from collections.abc import Iterator
from typing import Optional, cast
from math import gcd

def parse_notes(input_file: str) -> tuple[int, list[int | None]]:
    with open(input_file) as f:
        min_departure_ts = int(f.readline())
        bus_ids = [
            int(id) if id != 'x' else None 
            for id 
            in f.readline().split(',')
        ]
        return min_departure_ts, bus_ids

def calc_waiting_time(min_departure_ts: int, bus_freq: int) -> int:
    last_departure = min_departure_ts % bus_freq
    if last_departure == 0:
        return 0
    else:
        return bus_freq - last_departure

def get_earliest_bus(min_departure_ts: int, bus_ids: list[int]) -> tuple[int, int]:
    return min([
        (id, calc_waiting_time(min_departure_ts, id))
        for id
        in bus_ids
    ], key = lambda pair: pair[1])

def get_active_bus_ids(bus_ids: list[int | None]) -> list[int]:
    return [id for id in bus_ids if id is not None]

def yield_multiples(n: int) -> Iterator[int]:
    m = 0
    while True:
        yield m
        m += n

'''
Notes:

enumerate(bus_ids) = [(0, 7), (1, 13), _, _, (4, 59), _, (6, 31), (7, 19)]
    t % 7 == 0
    (t + 1) % 13 == 0
    (t + 4) % 59 == 0
    (t + 6) % 31 == 0
    (t + 7) % 19 == 0
'''

def get_earliest_sequence_departure_v1(bus_ids: list[int | None]) -> Optional[int]:
    '''
    Dumb solution: iterate the multiples of the first and get going. Too slow for real input.
    '''
    for t in yield_multiples(cast(int, bus_ids[0])):
        if t == 0:
            continue
        
        if all(
            calc_waiting_time(t, id) == idx 
            for idx, id 
            in enumerate(bus_ids) 
            if id is not None):
            return t

def get_earliest_sequence_departure_v2(bus_ids: list[int | None]) -> Optional[int]:
    '''
    Instead of trying out every multiple of the first, every time there's a mismatch
    Jump to the next plausible t for all of them and then recheck from the start.
    Too slow for real input.
    '''
    n = cast(int, bus_ids[0])
    t = n
    while True:
        requires_recheck = False
        for idx, id in enumerate(bus_ids):
            if id is None:
                continue

            waiting_time = calc_waiting_time(t + idx, id)
            if waiting_time > 0:
                requires_recheck = True
                # if the schedule does not match, let's find the next 't' where it does match
                # and continue, but mark that we need to recheck from the start 
                while waiting_time > 0:
                    # print('Schedule did not match, had to wait +', waiting_time, 'minutes for next bus', id)
                    # if the schedule does not match, when does the next bus 'id' leave?
                    min_next_t_for_id = t + waiting_time
                    # knowing that, when is the next departure from the first bus from then on?
                    t = min_next_t_for_id + calc_waiting_time(min_next_t_for_id, n)
                    # at that time, does the schedule of bus 'id' match?
                    waiting_time = calc_waiting_time(t + idx, id)
                
                # print('Jumping to time', t, 'compatible with bus ', id, 'leaving +', idx, 'minutes after the initial bus')
        
        if not requires_recheck:
            return t
        else:
            print('Restarting at time', t, 'after going through all the buses')

def get_earliest_sequence_departure_v3(bus_ids: list[int | None]) -> Optional[int]:
    '''
    Same as v2, but use the bus with higher frequency as the base to try to speed up the cycles
    Still too slow for real input, though.
    '''
    indexed_bus_ids = list((idx, bus_id) for idx, bus_id in enumerate(bus_ids) if bus_id is not None)
    hidx, highest_freq_bus = max(indexed_bus_ids, key = lambda pair: pair[1])
    print('Using bus', highest_freq_bus, 'as pivot, with schedule at t +', hidx)
    
    shifted_bus_ids = list((idx - hidx, bus_id) for idx, bus_id in indexed_bus_ids)
    n = highest_freq_bus
    t = n
    while True:
        requires_recheck = False
        for idx, id in shifted_bus_ids:
            waiting_time = calc_waiting_time(t + idx, id)
            if waiting_time > 0:
                requires_recheck = True
                # if the schedule does not match, let's find the next 't' where it does match
                # and continue, but mark that we need to recheck from the start 
                while waiting_time > 0:
                    # if the schedule does not match, when does the next bus 'id' leave?
                    min_next_t_for_id = t + waiting_time
                    # knowing that, when is the next departure from the first bus from then on?
                    t = min_next_t_for_id + calc_waiting_time(min_next_t_for_id, n)
                    # at that time, does the schedule of bus 'id' match?
                    waiting_time = calc_waiting_time(t + idx, id)
                
                # print('Jumping to time', t, 'compatible with bus ', id, 'leaving +', idx, 'minutes after the initial bus')
        
        if not requires_recheck:
            return t - hidx
        # else:
            # print('Restarting at time', t, 'after going through all the buses')


def get_earliest_sequence_departure(bus_ids: list[int|None]) -> Optional[int]:
    '''
    Same as v2, but use the bus with higher frequency as the base to try to speed up the cycles
    Still too slow for real input, though.
    '''
    indexed_bus_ids = list((idx, bus_id) for idx, bus_id in enumerate(bus_ids) if bus_id is not None)
    inv_sort_bus_ids = sorted(indexed_bus_ids, key = lambda pair: -pair[1])
    print(inv_sort_bus_ids)

    hidx, highest_freq_bus = inv_sort_bus_ids[0]
    print('Using bus', highest_freq_bus, 'as pivot, with schedule at t +', hidx)
    
    # pattern will repeat at the least common multiple of all numbers, so not worth checking that far
    gcd_bus_ids = gcd(*(id for _, id in indexed_bus_ids))
    lcm_bus_ids = reduce(lambda a, b: a * b[1], indexed_bus_ids, 1) // gcd_bus_ids
    print('gcd:', gcd_bus_ids, 'lcm:', lcm_bus_ids)

    shifted_bus_ids = list((idx - hidx, bus_id) for idx, bus_id in inv_sort_bus_ids[1:])
    n = highest_freq_bus
    t = n
    # cache = { }
    while t < lcm_bus_ids:
        # requires_recheck = False
        max_wait_time = max(calc_waiting_time(t + idx, id) for idx, id in shifted_bus_ids)
        if max_wait_time > 0:
            min_next_t = t + max_wait_time
            t = min_next_t + calc_waiting_time(min_next_t, n)
        else:
            return t - hidx
        # for idx, id in shifted_bus_ids:
        #     waiting_time = calc_waiting_time(t + idx, id)
        #     if waiting_time > 0:
        #         requires_recheck = True
        #         if id in cache and waiting_time in cache[id]:
        #             t += cache[id][waiting_time]
        #         else:
        #             first_waiting_time = waiting_time
        #             first_t = t

        #             # if the schedule does not match, let's find the next 't' where it does match
        #             # and continue, but mark that we need to recheck from the start 
        #             while waiting_time > 0:
        #                 # if the schedule does not match, when does the next bus 'id' leave?
        #                 min_next_t_for_id = t + waiting_time
        #                 # knowing that, when is the next departure from the first bus from then on?
        #                 t = min_next_t_for_id + calc_waiting_time(min_next_t_for_id, n)
        #                 # at that time, does the schedule of bus 'id' match?
        #                 waiting_time = calc_waiting_time(t + idx, id)

        #             if id not in cache:
        #                 cache[id] = { }
        #             cache[id][first_waiting_time] = t - first_t

        #         # print('Jumping to time', t, 'compatible with bus ', id, 'leaving +', idx, 'minutes after the initial bus')
        
        # if not requires_recheck:
        #     return t - hidx
        # # else:
            # print('Restarting at time', t, 'after going through all the buses')

def solve(input_file: str) -> None:
    print(f'[{input_file}]')
    full_path = path.join(path.dirname(__file__), input_file)

    min_departure_ts, bus_ids = parse_notes(full_path)
    bus_id, waiting_time = get_earliest_bus(min_departure_ts, get_active_bus_ids(bus_ids))
    print('Part 1 answer:', bus_id * waiting_time)

    earliest_t = get_earliest_sequence_departure(bus_ids)
    if earliest_t:
        print('Part 2 answer:', earliest_t)

    print()

if __name__ == '__main__':
    solve('example.txt')
    for i in range(2, 7):
        solve(f'example{i}.txt')
    solve('input.txt')