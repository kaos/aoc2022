from __future__ import annotations

from itertools import product

import pytest

from aoc.games.rock_paper_scissors.types import Move


@pytest.mark.parametrize(
    "move1, move2, win",
    [
        (Move.ROCK, Move.ROCK, None),
        (Move.ROCK, Move.PAPER, False),
        (Move.ROCK, Move.SCISSORS, True),
        (Move.PAPER, Move.ROCK, True),
        (Move.PAPER, Move.PAPER, None),
        (Move.PAPER, Move.SCISSORS, False),
        (Move.SCISSORS, Move.ROCK, False),
        (Move.SCISSORS, Move.PAPER, True),
        (Move.SCISSORS, Move.SCISSORS, None),
    ],
)
def test_win(move1: Move, move2: Move, win: bool | None) -> None:
    assert move1.win(move2) == win


@pytest.mark.parametrize(
    "opponent, desired_outcome",
    list(product((Move.ROCK, Move.PAPER, Move.SCISSORS), (True, False, None))),
)
def test_get_move(opponent: Move, desired_outcome: bool | None) -> None:
    assert opponent.get_move(desired_outcome).win(opponent) == desired_outcome
