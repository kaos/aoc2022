from underpants.engine import TestRulesEngine
from aoc.calories import rules, CaloriesInventoryRequest, CaloriesInventory


example_input = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def test_parse_cals_inventory() -> None:
    engine = TestRulesEngine.create_with_rules(
        *rules()
    )

    inventory = CaloriesInventory((
        6000,
        4000,
        11000,
        24000,
        10000,
    ))

    assert engine.request(CaloriesInventory, CaloriesInventoryRequest(example_input)) == inventory
    assert inventory.elf_carrying_most_calories() == (3, 24000)
