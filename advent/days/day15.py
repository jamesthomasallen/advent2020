from advent.util import read_data_int


def main(n_turn_1: int = 2020, n_turn_2: int = 30000000) -> list[int]:
    numbers = read_data_int('day15', ',')
    state, last_number, count = create_state(numbers)
    state, last_number_1, count = play_until(state, last_number, count, n_turn_1)
    state, last_number_2, count = play_until(state, last_number_1, count, n_turn_2)
    return [last_number_1, last_number_2]


def create_state(numbers: list[int]) -> tuple[dict[int, int], int, int]:
    state = {}
    count = -1
    for count, number in enumerate(numbers[:-1]):
        state[number] = count + 1
    return state, numbers[-1], count + 2


def play_until(state: dict[int, int], number: int, count: int, n_turn: int
               ) -> tuple[dict[int, int], int, int]:
    for count in range(count, n_turn):
        if number in state:
            next_number = count - state[number]
        else:
            next_number = 0
        state[number] = count
        number = next_number
    return state, number, count + 1
