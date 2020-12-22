from typing import Union

from advent.util import read_data


def main() -> list[Union[int, str]]:
    items = read_data('day21')
    items = process_items(items)
    allergens_map = infer_allergens(items)
    result_1 = count_not_allergens(items, allergens_map)
    result_2 = list_dangerous_ingredients(allergens_map)
    return [result_1, result_2]


def process_items(items: list[str]) -> list[dict[str, list[str]]]:
    return [process_item(item) for item in items]


def process_item(item: str) -> dict[str, list[str]]:
    ingredients, allergens = item.removesuffix(')').split(' (contains ')
    ingredients = ingredients.split(' ')
    allergens = allergens.split(', ')
    return {'ingredients': ingredients, 'allergens': allergens}


def infer_allergens(items: list[dict[str, list[str]]]) -> dict[str, str]:
    allergens_map = {}
    possible_map = {}
    n_allergen = len(set(sum((i['allergens'] for i in items), [])))
    while len(allergens_map) < n_allergen:
        for item in items:
            for allergen in [a for a in item['allergens'] if a not in allergens_map]:
                possible = [
                    ingredient for ingredient in item['ingredients']
                    if ingredient not in allergens_map.values()
                    and (
                        allergen not in possible_map or ingredient in possible_map[allergen]
                    )
                ]
                possible_map[allergen] = possible
                if len(possible) == 1:
                    allergens_map[allergen] = possible[0]
    return allergens_map


def count_not_allergens(items: list[dict[str, list[str]]], allergens_map: dict[str, str]) -> int:
    return sum(count_not_allergens_item(item, allergens_map) for item in items)


def count_not_allergens_item(item: dict[str, list[str]], allergens_map: dict[str, str]) -> int:
    return sum(ingredient not in allergens_map.values() for ingredient in item['ingredients'])


def list_dangerous_ingredients(allergens_map: dict[str, str]) -> str:
    return ','.join(
        ingredient for allergen, ingredient in sorted(allergens_map.items(), key=lambda x: x[0])
    )
