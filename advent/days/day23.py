from math import prod

from advent.util import read_data


def main() -> list[int]:
    cups, first_cup = initialise_cups(read_data('day23'))
    cups_1 = play_cups(cups, first_cup, 100)
    result_1 = as_int(get_after(cups_1, 1, len(cups_1)-1))
    cups_2 = extend_cups(cups, first_cup, 1000000)
    cups_2 = play_cups(cups_2, first_cup, 10000000)
    result_2 = prod(get_after(cups_2, 1, 2))
    return [result_1, result_2]


def initialise_cups(raw_cups: list[str]) -> tuple[dict[int, int], int]:
    cups_list = [int(i) for i in raw_cups[0]]
    n_cup = len(cups_list)
    return {cups_list[idx]: cups_list[(idx+1) % n_cup] for idx in range(n_cup)}, cups_list[0]


def play_cups(cups: dict[int, int], current_cup: int, n_turn: int, n_move: int = 3) -> dict[int, int]:
    cups = dict(cups)
    n_cup = len(cups)
    for i in range(n_turn):
        moving_cups = get_after(cups, current_cup, n_move)
        destination = get_destination(current_cup, moving_cups, n_cup)
        move_cups(cups, current_cup, moving_cups, destination)
        current_cup = cups[current_cup]
    return cups


def get_after(cups: dict[int, int], current_cup: int, n_move: int) -> list[int]:
    result = []
    for _ in range(n_move):
        current_cup = cups[current_cup]
        result.append(current_cup)
    return result


def get_destination(current_cup: int, moving_cups: list[int], n_cup: int) -> int:
    destination = current_cup - 1
    while destination in moving_cups or destination == 0:
        if destination in moving_cups:
            destination -= 1
        if destination == 0:
            destination = n_cup
    return destination


def move_cups(cups: dict[int, int], current_cup: int, moving_cups: list[int], destination: int) -> None:
    cups[current_cup] = cups[moving_cups[-1]]
    cups[moving_cups[-1]] = cups[destination]
    cups[destination] = moving_cups[0]


def as_int(cups_list: list[int]) -> int:
    return int(''.join(str(i) for i in cups_list))


def extend_cups(cups: dict[int, int], first_cup: int, n_cup: int) -> dict[int, int]:
    result = {}
    current_cup = first_cup
    for _ in range(len(cups)-1):
        result[current_cup] = cups[current_cup]
        current_cup = result[current_cup]
    result[current_cup] = len(cups) + 1
    for cup in range(len(cups)+1, n_cup):
        result[cup] = cup + 1
    result[n_cup] = first_cup
    return result
