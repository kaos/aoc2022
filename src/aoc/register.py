from aoc import calories
from aoc.games.rock_paper_scissors import rules as rock_paper_scissors
from aoc.packing.rucksack import rules as rucksack


def rules():
    return (*calories.rules(), *rock_paper_scissors.rules(), *rucksack.rules())
