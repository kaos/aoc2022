import click

from aoc.cargo.supplies import RawManifest, Stacks
from aoc.engine import request


@click.command
@click.argument("cargo_manifest", type=click.File())
@click.option(
    "--crane-model",
    type=click.Choice(["CrateMover-9000", "CrateMover-9001"]),
    default="CrateMover-9000",
)
def main(cargo_manifest, crane_model):
    cargo = request(
        Stacks, RawManifest(cargo_manifest.read(), crate_mover=crane_model.replace("-", ""))
    )
    print(f"Top crate of each stack are: {cargo.top_crate_ids()}.")
    if crane_model == "CrateMover-9000":
        print("\nPsst. This is the wrong crane model, try with --crane-model=CrateMover-9001\n\n")


if __name__ == "__main__":
    main()
