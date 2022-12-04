import click

from aoc.engine import request
from aoc.work.task_assignment import SectionAssignments, Teams


@click.command
@click.argument("assignments", type=click.File())
def main(assignments):
    teams = request(Teams, SectionAssignments(assignments.read()))
    print(f"There are {teams.fully_contained_work} pairs that fully contain the other.")
    print(f"There are {teams.partially_contained_work} pairs with ovelapping ranges.")


if __name__ == "__main__":
    main()
