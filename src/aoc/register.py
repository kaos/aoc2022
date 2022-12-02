from aoc import calories, games


def rules():
    return (*calories.rules(), *games.rules())
