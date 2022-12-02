from aoc import calories
from aoc.games.rock_paper_scissors import rules as rock_paper_scissors


def rules():
    return (*calories.rules(), *rock_paper_scissors.rules())
