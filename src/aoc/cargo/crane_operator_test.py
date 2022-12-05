from __future__ import annotations

import pytest
from underpants.engine import RulesEngine, TestRulesEngine

from aoc.cargo.crane_operator import StacksDrawing, rules
from aoc.cargo.supplies import RawManifest, Stacks

example_input = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


@pytest.fixture
def engine() -> RulesEngine:
    return TestRulesEngine.create_with_rules(*rules())


def test_crane_operator(engine: RulesEngine) -> None:
    stacks = engine.request(Stacks, RawManifest(example_input, "CrateMover9000"))
    assert stacks.top_crate_ids() == "CMZ"

    stacks = engine.request(Stacks, RawManifest(example_input, "CrateMover9001"))
    assert stacks.top_crate_ids() == "MCD"


def test_stacks_drawing() -> None:
    drawing = StacksDrawing(RawManifest(example_input, "").parsed_manifest()[0])
    cols = list(drawing.stack_columns())
    assert cols == [1, 5, 9]
    assert "".join(crate.id for crate in drawing.read_stack(cols[1])) == "DCM"
