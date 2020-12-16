from typing import Union
from itertools import combinations
from pathlib import Path
import re


def read_data(day: str, sep: str = '\n') -> list[str]:
    path = Path(__file__).parent.parent / 'data' / (day+'.txt')
    return path.read_text().strip().split(sep)


def read_data_int(day: str, sep: str = '\n') -> list[int]:
    return [int(i) for i in read_data(day, sep)]


def read_data_dict(day: str) -> list[dict]:
    return [
        dict(tuple(item.split(':')) for item in group.split())
        for group in read_data(day, sep='\n\n')
    ]


def read_data_list(day: str) -> list[list[str]]:
    return [group.split('\n') for group in read_data(day, sep='\n\n')]


def read_data_timetable(day: str) -> tuple[int, list[Union[str, int]]]:
    current_time_str, timetable_str = read_data(day)
    timetable = [x if x == 'x' else int(x) for x in timetable_str.split(',')]
    return int(current_time_str), timetable


def read_data_bitmask_instructions(day: str) -> list[dict[str, Union[str, int]]]:
    data = read_data(day)
    result = []
    for line in data:
        if match := re.match(r'mask = (?P<mask>[X01]+)', line):
            result.append({
                'type': 'mask',
                'mask': match.group('mask'),
            })
        elif match := re.match(r'mem\[(?P<address>\d+)] = (?P<value>\d+)', line):
            result.append({
                'type': 'write',
                'address': int(match.group('address')),
                'value': int(match.group('value')),
            })
        else:
            raise ValueError
    return result


def read_data_tickets(day: str) -> tuple[dict[str, list[tuple[int, int]]], list[int], list[list[int]]]:
    rules_str, my_ticket, nearby_tickets = read_data(day, sep='\n\n')
    rules = {}
    for rule in rules_str.split('\n'):
        name, ranges = rule.split(': ')
        rules[name] = []
        for range_str in ranges.split(' or '):
            rules[name].append(tuple(int(x) for x in range_str.split('-')))
    my_ticket = [int(x) for x in my_ticket.removeprefix('your ticket:\n').split(',')]
    nearby_tickets = [
        [int(x) for x in nearby.split(',')]
        for nearby in nearby_tickets.removeprefix('nearby tickets:\n').split('\n')
    ]
    return rules, my_ticket, nearby_tickets


def sum_to_target(numbers: list[int], target: int, n: int) -> tuple:
    for group in combinations(numbers, n):
        if sum(group) == target:
            return group
    raise RuntimeError('No group found to match target')
