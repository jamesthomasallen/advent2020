from math import prod

from advent.util import read_data_int, sum_to_target


def main(target: int = 2020, n_1: int = 2, n_2: int = 3) -> list[int]:
    expenses = read_data_int('day01')
    values_1 = sum_to_target(expenses, target, n_1)
    values_2 = sum_to_target(expenses, target, n_2)
    return [prod(values_1), prod(values_2)]
