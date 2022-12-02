from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    def win(self, opponent: Move) -> bool | None:
        # None indicates a draw.
        return None if self == opponent else self.value - 1 == (opponent.value % 3)

    def get_move(self, desired_outcome: bool | None) -> Move:
        return (
            self
            if desired_outcome is None
            else Move((self.value + (0 if desired_outcome else 1)) % 3 + 1)
        )


class Scoring:
    round_score = {
        True: 6,
        None: 3,
        False: 0,
    }

    @classmethod
    def score(cls, move: Move, win: bool | None) -> int:
        return move.value + cls.round_score[win]


@dataclass(frozen=True)
class GameRound:
    player_a: Move
    player_b: Move

    def score_player_a(self) -> int:
        return Scoring.score(self.player_a, self.player_a.win(self.player_b))

    def score_player_b(self) -> int:
        return Scoring.score(self.player_b, self.player_b.win(self.player_a))


@dataclass(frozen=True)
class Tournament:
    game_rounds: tuple[GameRound, ...]

    def total_score_player_a(self) -> int:
        return sum(map(GameRound.score_player_a, self.game_rounds))

    def total_score_player_b(self) -> int:
        return sum(map(GameRound.score_player_b, self.game_rounds))


@dataclass(frozen=True)
class TournamentRequest:
    strategy: str
