from __future__ import annotations

from underpants.engine import RulesEngine
from typing import TypeVar
import aoc.register  # noqa: F401


T = TypeVar("T")


def request(output: type[T], *inputs: Any, **engine_args) -> T:
    engine = RulesEngine.create(
        "aoc",
        backends=("aoc",),
        **engine_args,
    )
    with engine.pants_logging():
        with engine.new_session("aoc-session") as session:
            return session.request(output, *inputs)
