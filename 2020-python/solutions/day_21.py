"""AOC 2020 Day 21"""

import pathlib
import time
import collections

TEST_INPUT = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

TOP, RIGHT, BOTTOM, LEFT = 0, 1, 2, 3

def read_input(input_path: str) -> str:
    """take input file path and return a str with the file's content"""
    with open(input_path, 'r') as input_file:
        input_data = input_file.read().strip()
        return input_data

def extract(input_data: str) -> tuple:
    """take input data and return the appropriate data structure"""
    recipes = list()
    ingredient_allergenes = collections.defaultdict(set)
    recipes_with_allergene = collections.defaultdict(list)

    for index, recipe in enumerate(input_data.split('\n')):
        ingredients, allergenes = recipe.split(' (contains ')
        ingredients = set(ingredients.split())
        allergenes = set(allergenes.rstrip(')').split(', '))

        recipes.append(ingredients)
        for ingredient in ingredients:
            ingredient_allergenes[ingredient] |= allergenes
        for allergene in allergenes:
            recipes_with_allergene[allergene].append(index)

    return recipes, ingredient_allergenes, recipes_with_allergene

def find_safe_ingredients(recipes: list, ingredient_allergenes: dict, recipes_with_allergene: dict) -> list:
    """return a list of ingredients not containing allergenes"""
    safe_ingredients = list()
    for ingredient, allergenes in ingredient_allergenes.items():
        impossible_allergenes = set()
        for allergene in allergenes:
            if any(ingredient not in recipes[i] for i in recipes_with_allergene[allergene]):
                impossible_allergenes.add(allergene)
        allergenes -= impossible_allergenes
        if not allergenes:
            safe_ingredients.append(ingredient)
    return safe_ingredients

def assign_allergenes(ingredient_allergenes: dict) -> dict:
    """return a dict with each ingredient and its allergene"""
    assigned_allergenes = dict()
    while ingredient_allergenes:
        assigned_allergene = str()
        assigned_ingredient = str()

        for ingredient, allergenes in ingredient_allergenes.items():
            if len(allergenes) == 1:
                assigned_allergene = allergenes.pop()
                assigned_ingredient = ingredient
                break
        assigned_allergenes[assigned_allergene] = assigned_ingredient
        ingredient_allergenes.pop(assigned_ingredient)

        for ingredient, allergenes in ingredient_allergenes.items():
            if assigned_allergene in allergenes:
                allergenes.remove(assigned_allergene)

    return assigned_allergenes

def part1(entries: tuple) -> int:
    """part1 solver"""
    recipes, ingredient_allergenes, recipes_with_allergene = entries
    safe_ingredients = find_safe_ingredients(recipes, ingredient_allergenes, recipes_with_allergene)

    return sum(ingredient in recipe for recipe in recipes for ingredient in safe_ingredients)

def part2(entries: tuple) -> str:
    """part2 solver"""
    recipes, ingredient_allergenes, recipes_with_allergene = entries
    safe_ingredients = find_safe_ingredients(recipes, ingredient_allergenes, recipes_with_allergene)
    for ingredient in safe_ingredients:
        ingredient_allergenes.pop(ingredient)
    assigned_allergenes = assign_allergenes(ingredient_allergenes)

    return ','.join(map(assigned_allergenes.get, sorted(assigned_allergenes)))

def test_input_day_21():
    """pytest testing function"""
    entries = extract(TEST_INPUT)
    assert part1(entries) == 5
    assert part2(entries) == 'mxmxvkd,sqjhc,fvjkl'

def test_bench_day_21(benchmark):
    """pytest-benchmark function"""
    benchmark(main)

def main():
    """main function"""
    input_path = str(pathlib.Path(__file__).resolve().parent.parent) + "/inputs/" + str(pathlib.Path(__file__).stem)
    start_time = time.time()
    input_data = read_input(input_path)
    entries = extract(input_data)
    print("Part 1: %d" % part1(entries))
    print("Part 2: %s" % part2(entries))
    end_time = time.time()
    print("Execution time: %f" % (end_time-start_time))

if __name__ == "__main__":
    main()
