from aoc import calories
from aoc.cargo import crane_operator
from aoc.games.rock_paper_scissors import rules as rock_paper_scissors
from aoc.packing.rucksack import rules as rucksack
from aoc.work import task_assignment


def rules():
    return (
        *calories.rules(),
        *crane_operator.rules(),
        *rock_paper_scissors.rules(),
        *rucksack.rules(),
        *task_assignment.rules(),
    )
