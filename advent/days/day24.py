from collections import defaultdict

from advent.util import read_data


DIRECTIONS = {
    'e': (1, -1, 0),
    'w': (-1, 1, 0),
    'ne': (1, 0, -1),
    'sw': (-1, 0, 1),
    'nw': (0, 1, -1),
    'se': (0, -1, 1),
}


def main() -> list[int]:
    tiles_to_flip = read_data('day24')
    pattern = flip_tiles(tiles_to_flip)
    result_1 = len(pattern)
    pattern_100 = update_pattern(pattern, 100)
    result_2 = len(pattern_100)
    return [result_1, result_2]


def flip_tiles(tiles_to_flip: list[str]) -> list[tuple[int, int, int]]:
    flipped = []
    for tile_str in tiles_to_flip:
        tile_coords = process_coordinates(tile_str)
        if tile_coords not in flipped:
            flipped.append(tile_coords)
        else:
            flipped.remove(tile_coords)
    return flipped


def process_coordinates(tile_str: str) -> tuple[int, int, int]:
    steps = split_steps(tile_str)
    return take_steps(steps)


def split_steps(tile_str: str) -> list[str]:
    result = []
    idx = 0
    while idx < len(tile_str):
        n_char = 2 if tile_str[idx] in ('n', 's') else 1
        result.append(tile_str[idx:idx+n_char])
        idx += n_char
    return result


def take_steps(steps: list[str]) -> tuple[int, int, int]:
    result = (0, 0, 0)
    for step in steps:
        result = add_direction(result, step)
    return result


def update_pattern(pattern: list[tuple[int, int, int]], n_day: int) -> list[tuple[int, int, int]]:
    n_adjacent = count_adjacent(pattern)
    black = {tile: False for tile in n_adjacent}
    black.update({tile: True for tile in pattern})
    pattern = [
        tile for tile, n in n_adjacent.items()
        if (black[tile] and (0 < n <= 2)) or (not black[tile] and n == 2)
    ]
    if n_day == 1:
        return pattern
    else:
        return update_pattern(pattern, n_day-1)


def count_adjacent(pattern: list[tuple[int, int, int]]) -> dict[tuple[int, int, int], int]:
    n_adjacent = defaultdict(int)
    for tile in pattern:
        n_adjacent[tile] += 0
        for direction in DIRECTIONS:
            n_adjacent[add_direction(tile, direction)] += 1
    return dict(n_adjacent)


def add_direction(tile: tuple[int, ...], direction: str) -> tuple[int, ...]:
    return tuple(r + dr for r, dr in zip(tile, DIRECTIONS[direction]))
