import pytest
from underpants.engine import RulesEngine, TestRulesEngine

from aoc.packing.rucksack.rules import rules
from aoc.packing.rucksack.types import AnalysedContents, AnalysedContentsRequest

example_input = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


@pytest.fixture
def engine() -> RulesEngine:
    return TestRulesEngine.create_with_rules(*rules())


def test_example_input(engine: RulesEngine) -> None:
    analysed_contents = engine.request(AnalysedContents, AnalysedContentsRequest(example_input))
    assert analysed_contents.total_mispackaged == 157
