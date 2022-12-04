from aoc import calories
from aoc.games.rock_paper_scissors import rules as rock_paper_scissors
from aoc.packing.rucksack import rules as rucksack
from aoc.work import task_assignment


def rules():
    return (
        *calories.rules(),
        *rock_paper_scissors.rules(),
        *rucksack.rules(),
        *task_assignment.rules(),
    )
