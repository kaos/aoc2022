import click

from aoc.engine import request
from aoc.games import RockPaperScissors, TournamentStrategy


@click.command
@click.argument("strategy", type=click.File())
def main(strategy):
    tournament = request(RockPaperScissors.Tournament, TournamentStrategy(strategy.read()))
    print(
        f"According to the strategy guide, I would get a total score of {tournament.total_score_player_b()} points."
    )


if __name__ == "__main__":
    main()
