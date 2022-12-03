from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rucksack:
    compartments: tuple[str, ...]


@dataclass(frozen=True)
class RucksackRequest:
    contents: str


@dataclass(frozen=True)
class AnalysedContents:
    total_mispackaged: int


@dataclass(frozen=True)
class AnalysedContentsRequest:
    all_contents: str
