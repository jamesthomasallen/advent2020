from itertools import product

from advent.util import read_data


FLOOR = '.'
EMPTY = 'L'
OCCUP = '#'
DIRECTIONS = tuple(d for d in product([-1, 0, 1], [-1, 0, 1]) if d != (0, 0))


def main() -> list[int]:
    layout = read_data('day11')
    stable_layout_1 = step_until_stable(layout, 1, 4)
    n_occupied_1 = count_occupied(stable_layout_1)
    stable_layout_2 = step_until_stable(layout, 0, 5)
    n_occupied_2 = count_occupied(stable_layout_2)
    return [n_occupied_1, n_occupied_2]


def step_until_stable(layout: list[str], max_dist: int, thresh_high: int) -> list[str]:
    visible = map_visible(layout, max_dist)
    while True:
        next_layout = step(layout, visible, thresh_high)
        if next_layout == layout:
            return layout
        layout = next_layout


def step(layout: list[str], visible: list[list[list[tuple[int, int]]]], thresh_high: int) -> list[str]:
    n_adjacent = count_visible(layout, visible)
    return update_seats(layout, n_adjacent, thresh_high=thresh_high)


def count_visible(layout: list[str], visible: list[list[list[tuple[int, int]]]]) -> list[list[int]]:
    return [
        [
            sum(layout[y][x] == OCCUP for x, y in visible_list)
            for char, visible_list in zip(layout_row, visible_row)
        ]
        for layout_row, visible_row in zip(layout, visible)
    ]


def map_visible(layout: list[str], max_dist: int) -> list[list[list[tuple[int, int]]]]:
    max_y = len(layout)
    max_x = len(layout[0])
    if max_dist == 0:
        max_dist = max([max_x, max_y])
    visible = [[[] for _ in row] for row in layout]
    chair = [[c in (OCCUP, EMPTY) for c in row] for row in layout]
    for i, row in enumerate(chair):
        for j, c in enumerate(row):
            if c:
                for dx, dy in DIRECTIONS:
                    y, x = i, j
                    for dist in range(1, max_dist+1):
                        x += dx
                        y += dy
                        if x < 0 or y < 0 or x >= max_x or y >= max_y:
                            break
                        if chair[y][x]:
                            visible[y][x].append((j, i))
                            break
    return visible


def update_seats(layout: list[str], n_adjacent: list[list[int]],
                 thresh_low: int = 0, thresh_high: int = 4) -> list[str]:
    return [
        ''.join(
            OCCUP if char == EMPTY and n <= thresh_low else
            EMPTY if char == OCCUP and n >= thresh_high else
            char
            for char, n in zip(row, n_adj_row)
        )
        for row, n_adj_row in zip(layout, n_adjacent)
    ]


def count_occupied(layout: list[str]) -> int:
    return ''.join(layout).count(OCCUP)
