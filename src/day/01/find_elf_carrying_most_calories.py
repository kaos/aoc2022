import click

from aoc.calories import CaloriesInventory, CaloriesInventoryRequest
from aoc.engine import request


@click.command
@click.argument("inventory", type=click.File())
def main(inventory):
    inventory = request(CaloriesInventory, CaloriesInventoryRequest(inventory.read()))
    elf, cals = inventory.elf_carrying_most_calories()
    print(f"It is Elf #{elf+1} that is carrying the most calories, of {cals} cals.")


if __name__ == "__main__":
    main()
