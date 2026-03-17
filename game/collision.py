from __future__ import annotations

from typing import Iterable

GridPos = tuple[int, int]


def is_out_of_bounds(position: GridPos, cols: int, rows: int) -> bool:
    x_pos, y_pos = position
    return x_pos < 0 or x_pos >= cols or y_pos < 0 or y_pos >= rows


def is_self_collision(
    next_head: GridPos,
    occupied: Iterable[GridPos],
    tail: GridPos,
    will_grow: bool,
) -> bool:
    if next_head not in occupied:
        return False
    return will_grow or next_head != tail