from math import prod

from advent.util import read_data


SLOPE_1 = {'right': 3, 'down': 1}

SLOPES = [
    {'right': 1, 'down': 1},
    {'right': 3, 'down': 1},
    {'right': 5, 'down': 1},
    {'right': 7, 'down': 1},
    {'right': 1, 'down': 2},
]


def main() -> list[int]:
    tree_map = read_data('day03')
    n_tree_1 = count_trees(tree_map, SLOPE_1['right'], SLOPE_1['down'])
    result_2 = prod(count_trees(tree_map, s['right'], s['down']) for s in SLOPES)
    return [n_tree_1, result_2]


def count_trees(tree_map: list[str], right: int, down: int) -> int:
    width = len(tree_map[0])
    return sum(
        tree_line[(right * i) % width] == '#'
        for i, tree_line in enumerate(tree_map[::down])
    )
