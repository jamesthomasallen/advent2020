from advent.util import read_data


def main() -> list[int]:
    data = read_data('day02')
    n_valid_1 = count_valid(data, 1)
    n_valid_2 = count_valid(data, 2)
    return [n_valid_1, n_valid_2]


def count_valid(data: list[str], method: int) -> int:
    if method == 1:
        is_valid = is_valid_1
    elif method == 2:
        is_valid = is_valid_2
    else:
        raise ValueError(method)
    count = 0
    for row in data:
        rule, password = row.split(': ')
        if is_valid(password, rule):
            count += 1
    return count


def is_valid_1(password: str, rule: str) -> bool:
    allowed_min, allowed_max, letter = parse_rule(rule)
    return allowed_min <= password.count(letter) <= allowed_max


def is_valid_2(password: str, rule: str) -> bool:
    position_1, position_2, letter = parse_rule(rule)
    in_first = password[position_1-1] == letter
    in_second = password[position_2-1] == letter
    return in_first != in_second


def parse_rule(rule: str) -> tuple[int, int, str]:
    numbers, letter = rule.split()
    n_1, n_2 = [int(i) for i in numbers.split('-')]
    return n_1, n_2, letter
