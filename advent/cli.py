from typing import Callable
import importlib
import os
import pathlib

import click

import advent.results


@click.group()
def main():
    pass


def day_list() -> list[str]:
    return sorted([
        module_filename.removesuffix('.py')
        for module_filename in os.listdir(pathlib.Path(__file__).parent / 'days')
        if not module_filename.startswith('__')
    ])


def get_main(day: str) -> Callable[[], list]:
    day_module = importlib.import_module(f'advent.days.{day}')
    return day_module.main


def run_and_print(day: str) -> None:
    print(f'Day: {day}')
    for i, result in enumerate(get_main(day)()):
        print(f'Part {i+1}: {result}')


def check_and_print(day: str) -> None:
    print(f'Day: {day}')
    result_list = get_main(day)()
    expected_list = advent.results.RESULTS[day]
    for i, (result, expected) in enumerate(zip(result_list, expected_list)):
        outcome = 'PASS' if result == expected else 'FAIL'
        print(f'Part {i+1}: {outcome} result={result}, expected={expected}')


@main.command()
@click.argument('day')
def run(day: str) -> None:
    run_and_print(day)


@main.command()
def run_all() -> None:
    do_and_print_for_all(run_and_print)


@main.command()
def check_all() -> None:
    do_and_print_for_all(check_and_print)


def do_and_print_for_all(func: Callable[[str], None]) -> None:
    days = day_list()
    for day in days:
        func(day)
        if day != days[-1]:
            print()


if __name__ == '__main__':
    main()
