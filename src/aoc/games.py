from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from pants.engine.rules import QueryRule, collect_rules, rule


class RockPaperScissors:
    round_score = {
        True: 6,
        None: 3,
        False: 0,
    }

    class Move(Enum):
        ROCK = 1
        PAPER = 2
        SCISSORS = 3

        def win(self, against: RockPaperScissors.Move) -> bool | None:
            # None indicates a draw.
            return None if self == against else self.value - 1 == (against.value % 3)

        def score(self, against: RockPaperScissors.Move) -> int:
            return self.value + RockPaperScissors.round_score[self.win(against)]

    Rock = Move.ROCK
    Paper = Move.PAPER
    Scissors = Move.SCISSORS

    @dataclass(frozen=True)
    class GameRound:
        player_a: RockPaperScissors.Move
        player_b: RockPaperScissors.Move

        def score_player_a(self) -> int:
            return self.player_a.score(self.player_b)

        def score_player_b(self) -> int:
            return self.player_b.score(self.player_a)

    player_a_move_map = dict(
        A=Rock,
        B=Paper,
        C=Scissors,
    )
    player_b_move_map = dict(
        X=Rock,
        Y=Paper,
        Z=Scissors,
    )

    @classmethod
    def parse_round(cls, game_round: str) -> GameRound:
        player_a, player_b = game_round.split()
        return cls.new_round(cls.player_a_move_map[player_a], cls.player_b_move_map[player_b])

    @classmethod
    def new_round(cls, player_a: Move, player_b: Move) -> GameRound:
        return cls.GameRound(player_a, player_b)

    @dataclass(frozen=True)
    class Tournament:
        game_rounds: tuple[RockPaperScissors.GameRound, ...]

        def total_score_player_a(self) -> int:
            return sum(map(RockPaperScissors.GameRound.score_player_a, self.game_rounds))

        def total_score_player_b(self) -> int:
            return sum(map(RockPaperScissors.GameRound.score_player_b, self.game_rounds))

    @classmethod
    def parse_rounds(cls, game_rounds: str) -> Tournament:
        return cls.Tournament(tuple(map(cls.parse_round, game_rounds.splitlines())))


@dataclass(frozen=True)
class TournamentStrategy:
    game_rounds: str


@rule
def setup_tournament(strategy: TournamentStrategy) -> RockPaperScissors.Tournament:
    return RockPaperScissors.parse_rounds(strategy.game_rounds)


def rules():
    return (
        *collect_rules(),
        QueryRule(RockPaperScissors.Tournament, (TournamentStrategy,)),
    )
