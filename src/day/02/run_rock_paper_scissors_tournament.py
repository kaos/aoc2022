import click

from aoc.engine import request
from aoc.games.rock_paper_scissors.types import Tournament, TournamentRequest


@click.command
@click.argument("strategy", type=click.File())
@click.option("--part-two", is_flag=True, default=False)
def main(strategy, part_two):
    tournament = request(
        Tournament, TournamentRequest(strategy.read(), player_b_peek_at_a=part_two)
    )
    print(
        f"According to the strategy guide, I would get a total score of {tournament.total_score_player_b()} points."
    )

    if not part_two:
        print(
            "\nPsst. The Elf came back and told me how to interpret the second column of the strategy,"
            " run this again to get the correct answer:\n\n"
            "  ./pants run day-02 --part-two"
            "\n\n"
        )


if __name__ == "__main__":
    main()
