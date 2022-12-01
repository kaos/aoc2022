import click

from aoc.calories import CaloriesInventory, CaloriesInventoryRequest
from aoc.engine import request


@click.command
@click.argument("inventory", type=click.File())
def main(inventory):
    inventory = request(CaloriesInventory, CaloriesInventoryRequest(inventory.read()))
    elf, cals = inventory.elf_carrying_most_calories()
    print(f"It is Elf #{elf+1} that is carrying the most calories, of {cals} cals.")

    top_three = inventory.total_calories_carried_by(3)
    print(
        f"And of the 3 Elves carrying the most, the total number of calories carried is {top_three} cals."
    )


if __name__ == "__main__":
    main()
