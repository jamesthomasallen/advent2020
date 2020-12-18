from typing import Iterable, Union

from advent.util import read_data


def main() -> list[int]:
    equation_strs = read_data('day18')
    equations = interpret_equations(equation_strs)
    results_simple = solve_equations(equations, advanced=False)
    result_1 = sum(results_simple)
    results_advanced = solve_equations(equations, advanced=True)
    result_2 = sum(results_advanced)
    return [result_1, result_2]


def interpret_equations(equation_strs: list[str]) -> list[list]:
    return [interpret_equation(equation_str) for equation_str in equation_strs]


def interpret_equation(equation_str: str) -> list:
    tokens = equation_str.split()
    return list(interpret_tokens(tokens))


def interpret_tokens(tokens: list[str]) -> Iterable[Union[str, int, list]]:
    result = []
    active = [result]
    for idx, token in enumerate(tokens):
        while token.startswith('('):
            new_list = []
            active[-1].append(new_list)
            active.append(new_list)
            token = token[1:]
        if token in ('*', '+'):
            active[-1].append(token)
        else:
            active[-1].append(int(token.rstrip(')')))
        while token.endswith(')'):
            active = active[:-1]
            token = token[:-1]
    return result


def solve_equations(equations: list[list], advanced: bool) -> list[int]:
    return [solve_equation(equation, advanced) for equation in equations]


def solve_equation(equation: list, advanced: bool) -> int:
    equation = [solve_equation(e, advanced) if isinstance(e, list) else e for e in equation]
    while len(equation) > 1:
        idx = equation.index('+') if advanced and '+' in equation else 1
        equation = equation[:idx - 1] + [solve_binop(*equation[idx - 1:idx + 2])] + equation[idx + 2:]
    return equation[0]


def solve_binop(left, operator, right):
    if operator == '*':
        return left * right
    elif operator == '+':
        return left + right
    raise RuntimeError
