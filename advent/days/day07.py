import re

from advent.util import read_data


def main(my_colour: str = 'shiny gold') -> list[int]:
    rules_list = read_data('day07')
    rules = dict(parse_contents(rule_str) for rule_str in rules_list)
    count_mine = sum(can_contain(colour, my_colour, rules) for colour in rules)
    inside_mine = sum_inside(my_colour, rules)
    return [count_mine, inside_mine]


def parse_contents(rule: str) -> tuple[str, dict[str, int]]:
    colour, contents_str = rule.split(' bags contain ', 1)
    contents = {}
    if contents_str != 'no other bags.':
        for contents_i in contents_str.split(', '):
            match = re.match(r'(?P<number>\d+) (?P<colour>.*) bags?', contents_i)
            contents[match.group('colour')] = int(match.group('number'))
    return colour, contents


def can_contain(outer_colour: str, test_colour: str, rules: dict[str, dict[str, int]]) -> bool:
    this_rule = rules[outer_colour]
    return (
        bool(this_rule) and
        any(
            inner_colour == test_colour or
            can_contain(inner_colour, test_colour, rules)
            for inner_colour in this_rule
        )
    )


def sum_inside(colour: str, rules: dict[str, dict[str, int]]) -> int:
    return sum(
        sub_number * (1 + sum_inside(sub_colour, rules))
        for sub_colour, sub_number in rules[colour].items()
    )
