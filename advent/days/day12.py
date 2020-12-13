from advent.util import read_data


Position = tuple[int, int]
Facing = str

DIRECTIONS = ['N', 'E', 'S', 'W']


def main() -> list[int]:
    instructions = read_data('day12')
    position_wrong, facing = follow_instructions_wrong(instructions)
    distance_wrong = manhattan_distance(position_wrong)
    position_right, waypoint = follow_instructions_right(instructions)
    distance_right = manhattan_distance(position_right)
    return [distance_wrong, distance_right]


def follow_instructions_wrong(instructions: list[str]) -> tuple[Position, Facing]:
    position = (0, 0)
    facing = 'E'
    for instruction in instructions:
        position, facing = follow_instruction_wrong(instruction, position, facing)
    return position, facing


def follow_instruction_wrong(instruction: str, position: Position, facing: Facing
                             ) -> tuple[Position, Facing]:
    action, value = split_instruction(instruction)
    if action == 'F':
        action = facing
    if action in DIRECTIONS:
        position = follow_direction(position, action, value)
    elif action == 'L':
        facing = DIRECTIONS[(DIRECTIONS.index(facing) - int(value/90)) % 4]
    elif action == 'R':
        facing = DIRECTIONS[(DIRECTIONS.index(facing) + int(value/90)) % 4]
    return position, facing


def follow_instructions_right(instructions: list[str]) -> tuple[Position, Position]:
    position = (0, 0)
    waypoint = (10, 1)
    for instruction in instructions:
        position, waypoint = follow_instruction_right(instruction, position, waypoint)
    return position, waypoint


def follow_instruction_right(instruction: str, position: Position, waypoint: Position
                             ) -> tuple[Position, Position]:
    action, value = split_instruction(instruction)
    if action == 'F':
        position = (position[0] + value*waypoint[0], position[1] + value*waypoint[1])
    elif action in DIRECTIONS:
        waypoint = follow_direction(waypoint, action, value)
    elif action == 'L':
        for _ in range(int(value / 90)):
            waypoint = (-waypoint[1], waypoint[0])
    elif action == 'R':
        for _ in range(int(value / 90)):
            waypoint = (waypoint[1], -waypoint[0])
    return position, waypoint


def split_instruction(instruction: str) -> tuple[str, int]:
    return instruction[0], int(instruction[1:])


def follow_direction(position: Position, action: str, value: int) -> Position:
    if action == 'N':
        position = (position[0], position[1] + value)
    elif action == 'E':
        position = (position[0] + value, position[1])
    elif action == 'S':
        position = (position[0], position[1] - value)
    elif action == 'W':
        position = (position[0] - value, position[1])
    return position


def manhattan_distance(position: tuple[int, int]) -> int:
    return abs(position[0]) + abs(position[1])
