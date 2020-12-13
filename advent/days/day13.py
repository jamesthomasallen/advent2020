from typing import Union

from advent.util import read_data_timetable


def main() -> list[int]:
    current_time, buses = read_data_timetable('day13')
    next_bus, wait = find_next_bus(current_time, buses)
    result_1 = next_bus * wait
    timestamp = find_matching(buses)
    return [result_1, timestamp]


def find_next_bus(current_time: int, buses: list[Union[str, int]]) -> tuple[int, int]:
    wait = -1
    next_bus = -1
    for bus in (b for b in buses if isinstance(b, int)):
        this_wait = bus - (current_time % bus)
        if wait == -1 or this_wait < wait:
            wait = this_wait
            next_bus = bus
    if wait == -1:
        raise RuntimeError
    return next_bus, wait


def find_matching(buses: list[Union[str, int]]) -> int:
    requirements = sorted(
        ((i, b) for i, b in enumerate(buses) if isinstance(b, int)),
        key=lambda r: -r[1]
    )
    while len(requirements) > 1:
        requirements = [combine_requirements(*requirements[0], *requirements[1])] + requirements[2:]
    offset_combined, bus_combined = requirements[0]
    return (-offset_combined) % bus_combined


def combine_requirements(offset_0: int, bus_0: int, offset_1: int, bus_1: int) -> tuple[int, int]:
    bus_combined = lowest_common_multiple(bus_0, bus_1)
    timestamp = -offset_0
    while True:
        timestamp += bus_0
        assert ((timestamp + offset_0) % bus_0) == 0
        if ((timestamp + offset_1) % bus_1) == 0:
            offset_combined = bus_combined - timestamp
            return offset_combined, bus_combined


def lowest_common_multiple(bus_0: int, bus_1: int) -> int:
    result = bus_0
    while (result % bus_1) != 0:
        result += bus_0
    return result
