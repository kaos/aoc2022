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


def test_example_input_part_1(engine: RulesEngine) -> None:
    analysed_contents = engine.request(AnalysedContents, AnalysedContentsRequest(example_input, 1))
    assert analysed_contents.priority_sum == 157


def test_example_input_part_2(engine: RulesEngine) -> None:
    analysed_contents = engine.request(AnalysedContents, AnalysedContentsRequest(example_input, 3))
    assert analysed_contents.priority_sum == 70
