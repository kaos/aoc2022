import click

from aoc.engine import request
from aoc.packing.rucksack.types import AnalysedContents, AnalysedContentsRequest


@click.command
@click.argument("rucksack-contents", type=click.File())
def main(rucksack_contents):
    analysed_contents = request(AnalysedContents, AnalysedContentsRequest(rucksack_contents.read()))
    print(
        f"The sum of all the item priorities that was misplaced are {analysed_contents.total_mispackaged}"
    )


if __name__ == "__main__":
    main()
