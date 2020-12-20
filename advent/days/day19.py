from itertools import count
import re

from advent.util import read_data_list


UPDATES = {
    8: '42 | 42 8',
    11: '42 31 | 42 11 31'
}


def main() -> list[int]:
    rules, messages = read_data_list('day19')
    rules_dict = process_rules(rules)
    rule_0 = compile_rule(rules_dict, rules_dict[0])
    valid_messages = satisfies_rule_list(messages, rule_0)
    result_1 = sum(valid_messages)
    updated_rules_dict = dict(rules_dict)
    updated_rules_dict.update(UPDATES)
    compiled = compile_bottom_up(updated_rules_dict)
    valid_messages = satisfies_recursive_rule_0_list(messages, compiled)
    result_2 = sum(valid_messages)
    return [result_1, result_2]


def process_rules(rules: list[str]) -> dict[int, str]:
    result = {}
    for rule in rules:
        key, value = rule.split(': ')
        result[int(key)] = value
    return result


def compile_rule(rules_dict: dict[int, str], rule: str) -> str:
    if re.fullmatch(r'".*"', rule):
        return rule.strip('"')
    elif rule.isdigit():
        return compile_rule(rules_dict, rules_dict[int(rule)])
    elif ' | ' in rule:
        return '(' + '|'.join('(' + compile_rule(rules_dict, part) + ')' for part in rule.split(' | ')) + ')'
    elif ' ' in rule:
        return ''.join(compile_rule(rules_dict, part) for part in rule.split())
    return rule


def satisfies_rule_list(messages: list[str], compiled_rule: str) -> list[bool]:
    return [bool(re.fullmatch(compiled_rule, message)) for message in messages]


def compile_bottom_up(rules_dict: dict[int, str]) -> dict[int, str]:
    understood = {}
    n_understood = -1
    while n_understood != len(understood):
        n_understood = len(understood)
        understood.update({
            key: compile_rule(understood, rule)
            for key, rule in rules_dict.items()
            if key not in understood and (
                re.fullmatch(r'".*"', rule)
                or all(int(i) in understood for i in rule.split() if i.isdigit())
            )
        })
    return understood


def satisfies_recursive_rule_0_list(messages: list[str], rules_dict: dict[int, str]) -> list[bool]:
    return [satisfies_recursive_rule_0(message, rules_dict) for message in messages]


def satisfies_recursive_rule_0(message: str, rules_dict: dict[int, str]) -> bool:
    rule_42 = '(' + rules_dict[42] + ')'
    rule_31 = '(' + rules_dict[31] + ')'
    for n_31 in count(1):
        if not re.match(f'{rule_42}{{{n_31}}}', message):
            return False
        if re.fullmatch(f'{rule_42}+{rule_42}{{{n_31}}}{rule_31}{{{n_31}}}', message):
            return True
