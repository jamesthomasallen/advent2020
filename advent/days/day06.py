from advent.util import read_data_list


def main() -> list[int]:
    replies = read_data_list('day06')
    sum_distinct = sum(count_distinct(group) for group in replies)
    sum_all = sum(count_all(group) for group in replies)
    return [sum_distinct, sum_all]


def count_distinct(group: list[str]) -> int:
    return len(set(''.join(group)))


def count_all(group: list[str]) -> int:
    n_in_group = len(group)
    concatenated = ''.join(group)
    return sum(concatenated.count(char) == n_in_group for char in set(concatenated))
