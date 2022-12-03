import click

from aoc.engine import request
from aoc.packing.rucksack.types import AnalysedContents, AnalysedContentsRequest


@click.command
@click.argument("rucksack-contents", type=click.File())
@click.option(
    "--group-size",
    default=1,
    type=int,
    help="Part one is for individual rucksacks, i.e. group size of 1.",
)
def main(rucksack_contents, group_size):
    analysed_contents = request(
        AnalysedContents, AnalysedContentsRequest(rucksack_contents.read(), group_size)
    )
    print(f"The sum of all the item priorities are {analysed_contents.priority_sum}")

    if group_size == 1:
        print("\nPsst. For part two, run: `./pants run day-03 --group-size 3`\n")


if __name__ == "__main__":
    main()
