import click

from aoc.engine import request
from aoc.work.task_assignment import SectionAssignments, Teams


@click.command
@click.argument("assignments", type=click.File())
@click.option("--part-two", is_flag=True, default=False)
def main(assignments, part_two):
    teams = request(Teams, SectionAssignments(assignments.read()))
    print(f"There are {teams.fully_contained_work} pairs that fully contain the other.")

    if not part_two:
        print("?")


if __name__ == "__main__":
    main()
