from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from pants.engine.collection import Collection
from pants.engine.rules import QueryRule, collect_rules, rule


@dataclass(frozen=True)
class Assignment:
    section_ids: set[int]

    @classmethod
    def parse(cls, assignment: str) -> Assignment:
        section_start, section_stop = map(int, assignment.split("-"))
        return cls(set(range(section_start, section_stop + 1)))

    def __str__(self) -> str:
        graph = "".join(str(x) if x in self.section_ids else "." for x in range(1, 10))
        section_start = min(self.section_ids)
        section_stop = max(self.section_ids)
        return f"{graph}  {section_start}-{section_stop}"


@dataclass(frozen=True)
class Team:
    work: tuple[Assignment, ...]

    @classmethod
    def parse(cls, assignments: str) -> Team:
        return cls(tuple(Assignment.parse(assignment) for assignment in assignments.split(",")))

    def __str__(self) -> str:
        return "\n".join(str(assignment) for assignment in self.work)

    @property
    def contained_work(self) -> bool:
        return any(w1.section_ids.issubset(w2.section_ids) for w1, w2 in permutations(self.work, 2))

    @property
    def overlap_work(self) -> bool:
        return any(
            not w1.section_ids.isdisjoint(w2.section_ids) for w1, w2 in permutations(self.work, 2)
        )


class Teams(Collection[Team]):
    @classmethod
    def parse(cls, teams_assignments: str) -> Teams:
        return cls(tuple(Team.parse(assignments) for assignments in teams_assignments.splitlines()))

    @property
    def fully_contained_work(self) -> int:
        return sum(1 if team.contained_work else 0 for team in self)

    @property
    def partially_contained_work(self) -> int:
        return sum(1 if team.overlap_work else 0 for team in self)


@dataclass(frozen=True)
class SectionAssignments:
    raw: str


@rule
def parse_section_assignment_pairs(request: SectionAssignments) -> Teams:
    return Teams.parse(request.raw)


def rules():
    return (
        *collect_rules(),
        QueryRule(Teams, (SectionAssignments,)),
    )
