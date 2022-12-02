from __future__ import annotations

from dataclasses import dataclass

from pants.engine.rules import Get, MultiGet, QueryRule, collect_rules, rule
from pants.engine.unions import UnionRule, union

from aoc.games.rock_paper_scissors.types import GameRound, Move, Tournament, TournamentRequest


@dataclass(frozen=True)
class GameRoundRequest:
    player_a_strategy: str
    player_b_strategy: str


@union
@dataclass(frozen=True)
class MoveRequest:
    strategy: str


class PlayerAMoveRequest(MoveRequest):
    pass


class PlayerBMoveRequest(MoveRequest):
    pass


@rule
def get_player_a_move(request: PlayerAMoveRequest) -> Move:
    return Move(ord(request.strategy) - ord("A") + 1)


@rule
def get_player_b_move(request: PlayerBMoveRequest) -> Move:
    return Move(ord(request.strategy) - ord("X") + 1)


@rule
async def get_game_round(request: GameRoundRequest) -> GameRound:
    player_a_move = await Get(Move, MoveRequest, PlayerAMoveRequest(request.player_a_strategy))
    player_b_move = await Get(Move, MoveRequest, PlayerBMoveRequest(request.player_b_strategy))
    return GameRound(player_a_move, player_b_move)


@rule
async def setup_tournament(request: TournamentRequest) -> Tournament:
    rounds = await MultiGet(
        Get(GameRound, GameRoundRequest(*game_round_strategy.split()))
        for game_round_strategy in request.strategy.splitlines()
    )
    return Tournament(rounds)


def rules():
    return (
        *collect_rules(),
        QueryRule(Tournament, (TournamentRequest,)),
        UnionRule(MoveRequest, PlayerAMoveRequest),
        UnionRule(MoveRequest, PlayerBMoveRequest),
    )
