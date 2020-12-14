from typing import Union, Iterable
from collections import defaultdict
from itertools import product

from advent.util import read_data_bitmask_instructions


def main(mask_length: int = 36) -> list[int]:
    instructions = read_data_bitmask_instructions('day14')
    memory_1 = follow_instructions(instructions, mask_length, version=1)
    result_1 = sum_values(memory_1)
    memory_2 = follow_instructions(instructions, mask_length, version=2)
    result_2 = sum_values(memory_2)
    return [result_1, result_2]


def follow_instructions(instructions: list[dict[str, Union[str, int]]], mask_length: int,
                        version: int) -> dict[int, int]:
    mask = 'X' * mask_length
    memory = defaultdict(int)
    for instruction in instructions:
        mask, memory = follow_instruction(instruction, mask, memory, version=version)
    return memory


def follow_instruction(instruction: dict[str, Union[str, int]], mask: str, memory: dict[int, int],
                       version: int) -> tuple[str, dict[int, int]]:
    if instruction['type'] == 'mask':
        mask = instruction['mask']
    elif instruction['type'] == 'write':
        if version == 1:
            memory[instruction['address']] = force_values(instruction['value'], mask)
        elif version == 2:
            for address in apply_floating(instruction['address'], mask):
                memory[address] = instruction['value']
    return mask, memory


def force_values(value: int, mask: str) -> int:
    return force_ones(force_zeros(value, mask), mask)


def apply_floating(value: int, mask: str) -> Iterable[int]:
    value = force_ones(value, mask)
    for mask_floating in floating_masks(mask):
        yield force_values(value, mask_floating)


def floating_masks(mask: str) -> Iterable[str]:
    mask_template = mask.replace('X', '{}').replace('0', 'X').replace('1', 'X')
    for new_values in product('01', repeat=mask.count('X')):
        yield mask_template.format(*new_values)


def force_ones(value: int, mask: str) -> int:
    mask_or = int(mask.replace('X', '0'), base=2)
    return value | mask_or


def force_zeros(value: int, mask: str) -> int:
    mask_and = int(mask.replace('X', '1'), base=2)
    return value & mask_and


def sum_values(memory: dict[int, int]) -> int:
    return sum(memory.values())
