from advent.util import read_data


def main() -> list[int]:
    cards = read_data('day05')
    id_list = [seat_id(card) for card in cards]
    highest_id = max(id_list)
    my_id = find_missing_id(id_list)
    return [highest_id, my_id]


def seat_id(card: str, width: int = 8) -> int:
    row, column = seat_position(card)
    return row * width + column


def seat_position(card: str, lower_row: str = 'F', upper_row: str = 'B', lower_col: str = 'L',
                  upper_col: str = 'R', n_row_char: int = 7) -> tuple[int, int]:
    row_str, col_str = card[:n_row_char], card[n_row_char:]
    return (
        binary_partition(row_str, lower=lower_row, upper=upper_row),
        binary_partition(col_str, lower=lower_col, upper=upper_col),
    )


def binary_partition(code: str, lower: str, upper: str) -> int:
    if any(char not in (lower, upper) for char in code):
        raise ValueError(code)
    return sum(2**i if char == upper else 0 for i, char in enumerate(code[::-1]))


def find_missing_id(id_list: list[int]) -> int:
    for id_ in range(1, max(id_list)):
        if id_ not in id_list and (id_-1) in id_list and (id_+1) in id_list:
            return id_
    raise RuntimeError('No missing ID found')
