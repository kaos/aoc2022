from dataclasses import dataclass
from itertools import takewhile
from operator import itemgetter
from typing import Iterator, NewType

from pants.engine.rules import QueryRule, collect_rules, rule

Elf = NewType("Elf", int)
Calories = NewType("Calories", int)


@dataclass(frozen=True)
class CaloriesInventoryRequest:
    elves_inventories: str


@dataclass(frozen=True)
class CaloriesInventory:
    inventory: tuple[Calories, ...]

    def elf_carrying_most_calories(self) -> tuple[Elf, Calories]:
        idx, cals = max(enumerate(self.inventory), key=itemgetter(1))
        return Elf(idx), Calories(cals)


def split_inventory_per_elf(elves_inventories: str) -> Iterator[list[str]]:
    lines_it = iter(elves_inventories.splitlines())

    while True:
        elf_inventory = list(takewhile(bool, lines_it))
        if not elf_inventory:
            break
        yield elf_inventory


@rule
async def parse_calories_inventory(request: CaloriesInventoryRequest) -> CaloriesInventory:
    return CaloriesInventory(
        tuple(
            Calories(sum(map(int, elf_inventory)))
            for elf_inventory in split_inventory_per_elf(request.elves_inventories)
        )
    )


def rules():
    return (
        *collect_rules(),
        QueryRule(CaloriesInventory, (CaloriesInventoryRequest,)),
    )
