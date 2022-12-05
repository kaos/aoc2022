from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Iterator, Sequence

from pants.engine.collection import Collection
from pants.engine.rules import Get, MultiGet, QueryRule, collect_rules, rule

from aoc.cargo.supplies import Crate, RawManifest, Stack, Stacks


@dataclass(frozen=True)
class MoveCratesPlan:
    number_of_crates: int
    from_stack: int
    to_stack: int

    @classmethod
    def get_crate_mover(cls, name: str) -> type[MoveCratesPlan]:
        for mover in cls.__subclasses__():
            if mover.__name__ == name:
                return mover
        raise NotImplementedError()

    @staticmethod
    def _move_crates(crates: Sequence[Crate]) -> Iterable[Crate]:
        raise NotImplementedError()

    def execute(self, stacks: list[Stack]) -> Stacks:
        stacks[self.to_stack - 1] = Stack.create(
            tuple(self._move_crates(stacks[self.from_stack - 1][: self.number_of_crates]))
            + stacks[self.to_stack - 1]
        )
        stacks[self.from_stack - 1] = Stack.create(
            stacks[self.from_stack - 1][self.number_of_crates :]
        )
        return Stacks(stacks)


class CrateMover9000(MoveCratesPlan):
    @staticmethod
    def _move_crates(crates: Sequence[Crate]) -> Iterable[Crate]:
        return reversed(crates)


class CrateMover9001(MoveCratesPlan):
    @staticmethod
    def _move_crates(crates: Sequence[Crate]) -> Iterable[Crate]:
        return crates


@dataclass(frozen=True)
class MoveCratesRequest:
    plan: MoveCratesPlan
    stacks: Stacks


class Procedure(Collection[MoveCratesPlan]):
    @classmethod
    def create(cls, instructions: Iterable[MoveCratesPlan]) -> Procedure:
        return cls(tuple(instructions))


@dataclass(frozen=True)
class RearrangeStacksRequest:
    starting_layout: Stacks
    procedure: Procedure


@dataclass(frozen=True)
class StacksDrawing:
    drawing: tuple[str, ...]

    def stack_columns(self) -> Iterator[int]:
        for column, stack_id in enumerate(self.drawing[-1]):
            if stack_id.strip():
                yield column

    def read_stack(self, column: int) -> Iterator[Crate]:
        # Slicing `line` as that is safe, while indexing is not.
        for crate_id_box in (line[column : column + 1] for line in self.drawing[:-1]):
            if not crate_id_box:
                continue
            # Unbox sliced crate id
            crate_id = crate_id_box[0].strip()
            if crate_id:
                yield Crate(crate_id[0])


@dataclass(frozen=True)
class RawProcedure:
    instructions: tuple[str, ...]
    crate_mover: type[MoveCratesPlan]


@rule
def parse_stacks_drawing(stacks: StacksDrawing) -> Stacks:
    return Stacks.create(
        Stack.create(stacks.read_stack(column)) for column in stacks.stack_columns()
    )


@rule
def parse_procedure_instructions(procedure: RawProcedure) -> Procedure:
    return Procedure.create(
        procedure.crate_mover(*map(int, m.groups()))
        for m in (
            re.match(r"move (\d+) from (\d+) to (\d+)", line) for line in procedure.instructions
        )
        if m
    )


@rule
async def parse_manifest(raw: RawManifest) -> RearrangeStacksRequest:
    drawing, instructions = raw.parsed_manifest()
    stacks, procedure = await MultiGet(
        Get(Stacks, StacksDrawing(drawing)),
        Get(Procedure, RawProcedure(instructions, MoveCratesPlan.get_crate_mover(raw.crate_mover))),
    )
    return RearrangeStacksRequest(
        starting_layout=stacks,
        procedure=procedure,
    )


@rule
def move_crates(request: MoveCratesRequest) -> Stacks:
    return request.plan.execute(list(request.stacks))


@rule
async def crane_operator(work: RearrangeStacksRequest) -> Stacks:
    stacks = work.starting_layout
    for plan in work.procedure:
        stacks = await Get(Stacks, MoveCratesRequest(plan, stacks))
    return stacks


def rules():
    return (
        *collect_rules(),
        QueryRule(Stacks, (RawManifest,)),
    )
