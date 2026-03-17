from __future__ import annotations

import random

GridPos = tuple[int, int]


class Food:
    def __init__(self) -> None:
        self.position: GridPos = (0, 0)

    def respawn(self, cols: int, rows: int, forbidden: set[GridPos], rng: random.Random) -> GridPos:
        available = [
            (column, row)
            for column in range(cols)
            for row in range(rows)
            if (column, row) not in forbidden
        ]
        if not available:
            self.position = (0, 0)
            return self.position

        self.position = rng.choice(available)
        return self.position