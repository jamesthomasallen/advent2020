from collections.abc import Iterator

from advent.util import read_data


Instruction = tuple[str, int]


def main() -> list[int]:
    instructions = parse_instructions_list(read_data('day08'))
    try:
        boot(instructions, 0, 0, [])
    except InfiniteLoopException as ile:
        accumulator_broken = ile.args[0]
    else:
        raise RuntimeError
    accumulator_fixed = find_wrong_instruction(instructions)
    return [accumulator_broken, accumulator_fixed]


def parse_instructions_list(data: list[str]) -> list[Instruction]:
    return [parse_instruction(i) for i in data]


def parse_instruction(instruction_str: str) -> Instruction:
    operation, argument_str = instruction_str.split()
    return operation, int(argument_str)


def boot(instructions: list[Instruction], position: int, accumulator: int, history: list[int]) -> int:
    if position in history:
        raise InfiniteLoopException(accumulator)
    elif position == len(instructions):
        return accumulator
    else:
        history.append(position)
        position, accumulator = step(instructions, position, accumulator)
        return boot(instructions, position, accumulator, history)


def step(instructions: list[Instruction], position: int, accumulator: int) -> tuple[int, int]:
    operation, argument = instructions[position]
    if operation == 'acc':
        accumulator += argument
        position += 1
    elif operation == 'jmp':
        position += argument
    elif operation == 'nop':
        position += 1
    else:
        raise ValueError(operation)
    return position, accumulator


def find_wrong_instruction(instructions: list[Instruction]) -> int:
    for instructions_test in swap_each_jmp_nop(instructions):
        try:
            return boot(instructions_test, 0, 0, [])
        except InfiniteLoopException:
            pass


def swap_each_jmp_nop(instructions: list[Instruction]) -> Iterator[list[Instruction]]:
    for i in range(len(instructions)):
        before, instr, after = instructions[:i], instructions[i], instructions[i+1:]
        operation, argument = instr
        if operation in ('jmp', 'nop'):
            operation = 'nop' if operation == 'jmp' else 'jmp'
            instructions_test = before + [(operation, argument)] + after
            yield instructions_test


class InfiniteLoopException(Exception):
    pass
