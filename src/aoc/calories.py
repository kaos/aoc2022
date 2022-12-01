from dataclasses import dataclass
from itertools import islice, takewhile
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
        return self._get_max(self.inventory)

    def top_elves_carrying_most_calories(self) -> Iterator[tuple[Elf, Calories]]:
        inventory = self.inventory
        for _ in range(len(inventory)):
            elf, cals = self._get_max(inventory)
            yield elf, cals
            inventory = inventory[:elf] + (Calories(0),) + inventory[elf + 1 :]

    def total_calories_carried_by(self, top_elves: int) -> Calories:
        return Calories(
            sum(map(itemgetter(1), islice(self.top_elves_carrying_most_calories(), top_elves)))
        )

    @staticmethod
    def _get_max(inventory: tuple[Calories, ...]) -> tuple[Elf, Calories]:
        idx, cals = max(enumerate(inventory), key=itemgetter(1))
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
