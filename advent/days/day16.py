from math import prod

from advent.util import read_data_tickets


def main() -> list[int]:
    rules, my_ticket, nearby_tickets = read_data_tickets('day16')
    invalid = find_invalid_values(nearby_tickets, rules)
    result_1 = sum(sum(invalid, []))
    field_order = find_field_order([t for t, i in zip(nearby_tickets, invalid) if not i], rules)
    result_2 = prod(v for v, f in zip(my_ticket, field_order) if f.startswith('departure'))
    return [result_1, result_2]


def find_invalid_values(nearby_tickets: list[list[int]], rules: dict[str, list[tuple[int, int]]]
                        ) -> list[list[int]]:
    return [
        [value for value in ticket if not in_any_range(value, rules)]
        for ticket in nearby_tickets
    ]


def in_any_range(value: int, rules: dict[str, list[tuple[int, int]]]) -> bool:
    return any(satisfies_rule(value, ranges) for ranges in rules.values())


def satisfies_rule(value: int, ranges: list[tuple[int, int]]) -> bool:
    return any(lower <= value <= upper for lower, upper in ranges)


def find_field_order(tickets: list[list[int]], rules: dict[str, list[tuple[int, int]]]) -> list[str]:
    options = [
        [
            field for field, ranges in rules.items()
            if all(satisfies_rule(ticket[i], ranges) for ticket in tickets)
        ]
        for i in range(len(rules))
    ]
    while any(len(o) > 1 for o in options):
        singletons = [o[0] for o in options if len(o) == 1]
        options = [
            [field for field in o if field not in singletons] if len(o) > 1 else o
            for o in options
        ]
    return [o[0] for o in options]
