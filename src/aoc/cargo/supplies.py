from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pants.engine.collection import Collection


@dataclass(frozen=True)
class Crate:
    id: str


class Stack(Collection[Crate]):
    @classmethod
    def create(cls, crates: Iterable[Crate]) -> Stack:
        return cls(tuple(crates))


class Stacks(Collection[Stack]):
    @classmethod
    def create(cls, stacks: Iterable[Stack]) -> Stacks:
        return cls(tuple(stacks))

    def top_crate_ids(self) -> str:
        return "".join(stack[0].id for stack in self)


@dataclass(frozen=True)
class RawManifest:
    """The manifest is in two sections, beginning with a drawing of stacks
    followed by the procedures in how to move the stacked crates around."""

    manifest: str

    def parsed_manifest(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        lines = self.manifest.splitlines()
        section_break = lines.index("")
        return tuple(lines[:section_break]), tuple(lines[section_break + 1 :])
