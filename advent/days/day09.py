from advent.util import read_data_int, sum_to_target


def main(window: int = 25) -> list[int]:
    numbers = read_data_int('day09')
    first_bad = find_first_bad(numbers, window)
    contiguous = find_contiguous_sum(numbers, first_bad)
    result = min(contiguous) + max(contiguous)
    return [first_bad, result]


def find_first_bad(numbers: list[int], window: int) -> int:
    for i in range(window, len(numbers)):
        try:
            sum_to_target(numbers[i-window:i], numbers[i], 2)
        except RuntimeError:
            return numbers[i]


def find_contiguous_sum(numbers: list[int], target: int) -> list[int]:
    for start in range(len(numbers)):
        for finish in range(start+1, len(numbers)):
            current_sum = sum(numbers[start:finish])
            if current_sum == target:
                return numbers[start:finish]
            elif current_sum > target:
                break
            else:
                continue
