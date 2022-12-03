from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rucksack:
    compartments: tuple[str, ...]


@dataclass(frozen=True)
class RucksackRequest:
    contents: str
    compartments: int


@dataclass(frozen=True)
class AnalysedContents:
    priority_sum: int


@dataclass(frozen=True)
class AnalysedContentsRequest:
    all_contents: str
    group_size: int
