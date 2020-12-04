from itertools import combinations
from math import prod

from advent.util import read_data_int


def main(target: int = 2020, n_1: int = 2, n_2: int = 3) -> list[int]:
    expenses = read_data_int('day01')
    values_1 = sum_to_target(expenses, target, n_1)
    values_2 = sum_to_target(expenses, target, n_2)
    return [prod(values_1), prod(values_2)]


def sum_to_target(expenses: list[int], target: int, n: int) -> tuple:
    for group in combinations(expenses, n):
        if sum(group) == target:
            return group
    raise RuntimeError('No group found to match target')
