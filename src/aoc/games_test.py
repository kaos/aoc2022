import pytest
from underpants.engine import RulesEngine, TestRulesEngine

from aoc.games import RockPaperScissors, rules

example_input = """\
A Y
B X
C Z
"""

Rock = RockPaperScissors.Rock
Paper = RockPaperScissors.Paper
Scissors = RockPaperScissors.Scissors


@pytest.fixture
def engine() -> RulesEngine:
    return TestRulesEngine.create_with_rules(*rules())


@pytest.fixture
def tournament() -> RockPaperScissors.Tournament:
    return RockPaperScissors.parse_rounds(example_input)


def test_game_rounds(tournament: RockPaperScissors.Tournament) -> None:
    assert tournament.game_rounds == (
        RockPaperScissors.new_round(Rock, Paper),
        RockPaperScissors.new_round(Paper, Rock),
        RockPaperScissors.new_round(Scissors, Scissors),
    )


def test_score(tournament: RockPaperScissors.Tournament) -> None:
    assert [game_round.score_player_b() for game_round in tournament.game_rounds] == [8, 1, 6]


def test_tournament(tournament: RockPaperScissors.Tournament) -> None:
    assert tournament.total_score_player_b() == 15
