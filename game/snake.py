from __future__ import annotations

from collections import deque
from typing import Deque

GridPos = tuple[int, int]
Direction = tuple[int, int]


class Snake:
    """Snake state container with movement rules and render interpolation history."""

    DIRECTION_MAP: dict[str, Direction] = {
        "up": (0, 1),
        "down": (0, -1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    def __init__(self, start: GridPos, length: int = 4) -> None:
        self.segments: Deque[GridPos] = deque()
        self.previous_segments: list[GridPos] = []
        self.occupied: set[GridPos] = set()
        self.direction: Direction = self.DIRECTION_MAP["right"]
        self.pending_direction: Direction = self.direction
        self.reset(start, length)

    def reset(self, start: GridPos, length: int) -> None:
        """Recreate a horizontal snake centered at the provided start position."""
        self.direction = self.DIRECTION_MAP["right"]
        self.pending_direction = self.direction
        self.segments = deque((start[0] - offset, start[1]) for offset in range(length))
        self.previous_segments = list(self.segments)
        self.occupied = set(self.segments)

    @property
    def head(self) -> GridPos:
        return self.segments[0]

    @property
    def tail(self) -> GridPos:
        return self.segments[-1]

    def request_direction(self, direction_name: str) -> bool:
        """Queue a direction change, rejecting illegal reverse turns."""
        new_direction = self.DIRECTION_MAP.get(direction_name)
        if new_direction is None:
            return False

        if self._is_reverse(self.direction, new_direction):
            return False

        self.pending_direction = new_direction
        return True

    def next_head(self) -> GridPos:
        delta_x, delta_y = self.pending_direction
        return self.head[0] + delta_x, self.head[1] + delta_y

    def move(self, grow: bool = False, forced_head: "GridPos | None" = None) -> None:
        """Advance one step and optionally force the next head (used for wrap moves)."""
        self.previous_segments = list(self.segments)
        self.direction = self.pending_direction
        new_head = forced_head if forced_head is not None else self.next_head()
        self.segments.appendleft(new_head)
        self.occupied.add(new_head)

        if not grow:
            removed = self.segments.pop()
            self.occupied.discard(removed)

    def get_interpolated_segments(
        self, alpha: float, cols: int = 0, rows: int = 0
    ) -> list[tuple[float, float]]:
        """Return smooth in-between segment positions for the current render frame."""
        interpolated: list[tuple[float, float]] = []
        for index, current in enumerate(self.segments):
            previous = self.previous_segments[index] if index < len(self.previous_segments) else current
            prev_x = float(previous[0])
            prev_y = float(previous[1])
            curr_x = float(current[0])
            curr_y = float(current[1])

            # Interpolate on a torus so edge crossing is smooth in both axes.
            if cols > 0 and abs(curr_x - prev_x) > cols / 2:
                curr_x += cols if curr_x < prev_x else -cols
            if rows > 0 and abs(curr_y - prev_y) > rows / 2:
                curr_y += rows if curr_y < prev_y else -rows

            x_pos = prev_x + (curr_x - prev_x) * alpha
            y_pos = prev_y + (curr_y - prev_y) * alpha

            if cols > 0:
                x_pos %= cols
            if rows > 0:
                y_pos %= rows

            interpolated.append((x_pos, y_pos))
        return interpolated

    @staticmethod
    def _is_reverse(current: Direction, new_direction: Direction) -> bool:
        return current[0] + new_direction[0] == 0 and current[1] + new_direction[1] == 0