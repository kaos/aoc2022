from __future__ import annotations

from aoc.cargo.supplies import RawManifest

example_input = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def test_parse_raw_manifest() -> None:
    manifest = RawManifest(example_input)
    sections = manifest.parsed_manifest()
    lines = example_input.splitlines()
    assert sections[0] == tuple(lines[:4])
    assert sections[1] == tuple(lines[5:])
