import pytest
from underpants.engine import RulesEngine, TestRulesEngine

from aoc.work.task_assignment import SectionAssignments, Teams, rules

example_input = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

pretty_print_assignments = """\
.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8\
"""


@pytest.fixture
def engine() -> RulesEngine:
    return TestRulesEngine.create_with_rules(*rules())


def test_example_input_part_1(engine: RulesEngine) -> None:
    teams = engine.request(Teams, SectionAssignments(example_input))
    assert "\n\n".join(str(team) for team in teams) == pretty_print_assignments
    assert teams.fully_contained_work == 2
