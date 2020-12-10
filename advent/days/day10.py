from collections import defaultdict
from collections.abc import Iterator
from functools import cache
from itertools import combinations
from math import prod

from advent.util import read_data_int


def main(outlet_rating: int = 0, device_diff: int = 3) -> list[int]:
    joltages = read_data_int('day10')
    joltages = sort_joltages(joltages, outlet_rating, device_diff)
    diff_count = count_differences(joltages)
    result_1 = diff_count[1] * diff_count[3]
    arrangements = count_arrangements(joltages)
    return [result_1, arrangements]


def count_differences(joltages: list[int]) -> dict[int, int]:
    result = defaultdict(int)
    for i in range(1, len(joltages)):
        result[joltages[i] - joltages[i-1]] += 1
    return dict(result)


def count_arrangements(joltages: list[int], max_diff: int = 3) -> int:
    chunks = chunk_joltages(joltages, max_diff)
    return prod(count_arrangements_chunk(chunk, max_diff) for chunk in chunks)


def sort_joltages(joltages: list[int], outlet_rating: int = 0, device_diff: int = 3,
                  ) -> list[int]:
    return [outlet_rating] + sorted(joltages) + [max(joltages) + device_diff]


def chunk_joltages(joltages: list[int], max_diff: int) -> list[list[int]]:
    result = []
    diffs = [joltages[i] - joltages[i-1] for i in range(1, len(joltages))]
    while joltages:
        if max_diff in diffs:
            index = diffs.index(max_diff) + 1
        else:
            index = len(joltages)
        result.append(joltages[:index])
        joltages = joltages[index:]
        diffs = diffs[index:]
    return result


def count_arrangements_chunk(chunk: list[int], max_diff: int) -> int:
    if len(chunk) <= 2:
        return 1
    first = chunk[0]
    chunk_zeroed = tuple(i-first for i in chunk)
    return count_arrangements_chunk_zeroed(chunk_zeroed, max_diff)


@cache
def count_arrangements_chunk_zeroed(chunk: tuple[int], max_diff: int) -> int:
    first, middle, last = chunk[0], chunk[1:-1], chunk[-1]
    return sum(
        max_difference((first,) + sub_items + (last,)) <= max_diff
        for sub_items in all_combinations(middle)
    )


def max_difference(items: tuple[int]) -> int:
    return max(items[i] - items[i-1] for i in range(1, len(items)))


def all_combinations(items: tuple) -> Iterator[tuple]:
    for n in range(len(items)+1):
        yield from combinations(items, n)
