from itertools import islice

from underpants.engine import TestRulesEngine

from aoc.calories import Calories, CaloriesInventory, CaloriesInventoryRequest, Elf, rules

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
    engine = TestRulesEngine.create_with_rules(*rules())

    inventory = CaloriesInventory(
        (
            Calories(6000),
            Calories(4000),
            Calories(11000),
            Calories(24000),
            Calories(10000),
        )
    )

    assert engine.request(CaloriesInventory, CaloriesInventoryRequest(example_input)) == inventory
    assert inventory.elf_carrying_most_calories() == (Elf(3), Calories(24000))
    assert list(islice(inventory.top_elves_carrying_most_calories(), 3)) == [
        (Elf(3), Calories(24000)),
        (Elf(2), Calories(11000)),
        (Elf(4), Calories(10000)),
    ]
    assert inventory.total_calories_carried_by(3) == Calories(45000)
