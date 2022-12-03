from __future__ import annotations

from dataclasses import dataclass
from functools import reduce

from pants.engine.rules import Get, MultiGet, QueryRule, collect_rules, rule

from aoc.packing.rucksack.types import (
    AnalysedContents,
    AnalysedContentsRequest,
    Rucksack,
    RucksackRequest,
)

item_priority_map = {
    chr(item): item - base
    for base, items in (
        (ord("a") - 1, range(ord("a"), ord("z") + 1)),
        (ord("A") - 27, range(ord("A"), ord("Z") + 1)),
    )
    for item in items
}


def item_type_priority(item: str) -> int:
    return item_priority_map[item]


@dataclass(frozen=True)
class AnalysedRucksack:
    common_item_types: str

    @property
    def priority(self) -> int:
        return sum(map(item_type_priority, self.common_item_types))


@rule
def analyse_rucksack(rucksack: Rucksack) -> AnalysedRucksack:
    compartments = [set(compartment) for compartment in rucksack.compartments]
    return AnalysedRucksack(
        "".join(
            reduce(set.intersection, compartments[1:], compartments[0])  # type: ignore[arg-type]
        )
    )


@rule
def parse_rucksack_contents(request: RucksackRequest) -> Rucksack:
    middle = len(request.contents) // 2
    return Rucksack((request.contents[:middle], request.contents[middle:]))


@rule
async def analyse_contents(request: AnalysedContentsRequest) -> AnalysedContents:
    rucksacks = await MultiGet(
        Get(AnalysedRucksack, RucksackRequest(contents))
        for contents in request.all_contents.splitlines()
    )

    return AnalysedContents(sum(rucksack.priority for rucksack in rucksacks))


def rules():
    return (
        *collect_rules(),
        QueryRule(AnalysedContents, (AnalysedContentsRequest,)),
    )
