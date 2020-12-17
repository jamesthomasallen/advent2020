from typing import Any, Iterable
from copy import deepcopy
from itertools import product

from advent.util import read_data


INACT = '.'
ACTIV = '#'


def main(n_step: int = 6) -> list[int]:
    cubes_flat = read_data('day17')
    cubes_flat = [list(row) for row in cubes_flat]
    cubes_3d = [cubes_flat]
    cubes_3d = take_n_steps(cubes_3d, n_step)
    result_1 = count_active(cubes_3d)
    cubes_4d = [[cubes_flat]]
    cubes_4d = take_n_steps(cubes_4d, n_step)
    result_2 = count_active(cubes_4d)
    return [result_1, result_2]


def take_n_steps(cubes: list, n_step: int) -> list:
    for _ in range(n_step):
        cubes = take_step(cubes)
    return cubes


def take_step(cubes: list) -> list:
    n_adjacent = count_adjacent(cubes)
    cubes = expand_cubes(cubes)
    cubes = update_active(cubes, n_adjacent)
    cubes = trim_inactive(cubes)
    return cubes


def count_adjacent(cubes: list) -> list:
    dims = get_dims(cubes)
    count = repeated_slice(0, [d + 2 for d in dims])
    for x in product(*(range(d) for d in dims)):
        if nested_get(cubes, x) == ACTIV:
            for dx in directions(len(dims)):
                x2 = tuple(x_i + dx_i + 1 for x_i, dx_i in zip(x, dx))
                nested_get(count, x2[:-1])[x2[-1]] += 1
    return count


def nested_get(cubes: list, x: tuple) -> Any:
    while x:
        cubes = cubes[x[0]]
        x = x[1:]
    return cubes


def directions(n: int) -> Iterable[tuple[int]]:
    stationary = (0,) * n
    return (d for d in product([-1, 0, 1], repeat=n) if d != stationary)


def update_active(cubes: list, n_adjacent: list, min_active: int = 2, max_active: int = 3,
                  min_inactive: int = 3, max_inactive: int = 3) -> list:
    return [
        update_active(
            sub_cubes, sub_n,
            min_active=min_active, max_active=max_active,
            min_inactive=min_inactive, max_inactive=max_inactive,
        ) if isinstance(sub_cubes, list)
        else ACTIV if (
            (sub_cubes == ACTIV and min_active <= sub_n <= max_active) or
            (sub_cubes == INACT and min_inactive <= sub_n <= max_inactive)
        )
        else INACT
        for sub_cubes, sub_n in zip(cubes, n_adjacent)
    ]


def expand_cubes(cubes: list) -> list:
    if isinstance(cubes, list):
        meat = [expand_cubes(c) for c in cubes]
        bread = repeated_slice(INACT, [d + 2 for d in get_dims(cubes)[1:]])
        return [bread] + meat + deepcopy([bread])
    else:
        return cubes


def repeated_slice(var: Any, dims: list[int]) -> list:
    if not dims:
        return var
    result = [var for _ in range(dims[-1])]
    for dim in dims[:-1][::-1]:
        result = [deepcopy(result) for _ in range(dim)]
    return result


def trim_inactive(cubes: list):
    dims = get_dims(cubes)
    for direction, dim in enumerate(dims):
        while count_active(get_slice(cubes, direction, 0)) == 0:
            cubes = remove_slice(cubes, direction, 0)
        while count_active(get_slice(cubes, direction, -1)) == 0:
            cubes = remove_slice(cubes, direction, -1)
    return cubes


def get_slice(cubes: list, direction: int, idx: int) -> list:
    if direction == 0:
        return cubes[idx]
    else:
        return [get_slice(sub_cubes, direction-1, idx) for sub_cubes in cubes]


def remove_slice(cubes: list, direction: int, idx: int) -> list:
    if direction == 0:
        if idx < 0:
            idx = len(cubes) + idx
        return [sub_cubes for i, sub_cubes in enumerate(cubes) if i != idx]
    else:
        return [remove_slice(sub_cubes, direction-1, idx) for sub_cubes in cubes]


def count_active(cubes: list) -> int:
    return join(cubes).count(ACTIV)


def join(cubes: list) -> str:
    while isinstance(cubes[0], list):
        cubes = sum(cubes, [])
    return ''.join(cubes)


def get_dims(cubes: list) -> list[int]:
    result = [len(cubes)]
    if isinstance(cubes[0], list):
        result.extend(get_dims(cubes[0]))
    return result
