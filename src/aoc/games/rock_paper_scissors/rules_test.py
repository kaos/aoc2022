import pytest
from underpants.engine import RulesEngine, TestRulesEngine

from aoc.games.rock_paper_scissors.rules import rules
from aoc.games.rock_paper_scissors.types import Tournament, TournamentRequest

example_input = """\
A Y
B X
C Z
"""


@pytest.fixture
def engine() -> RulesEngine:
    return TestRulesEngine.create_with_rules(*rules())


def test_example_input(engine: RulesEngine) -> None:
    tournament = engine.request(Tournament, TournamentRequest(example_input))
    assert [game_round.score_player_b() for game_round in tournament.game_rounds] == [8, 1, 6]
    assert tournament.total_score_player_b() == 15
