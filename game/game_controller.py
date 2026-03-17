from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable

from game import settings
from game.collision import is_self_collision
from game.food import Food
from game.snake import Snake
from utils.score_manager import ScoreManager

GridPos = tuple[int, int]
FoodCallback = Callable[[GridPos, int], None]
ScoreCallback = Callable[[int, int], None]
PauseCallback = Callable[[bool], None]
GameOverCallback = Callable[[int, int], None]


@dataclass(slots=True)
class GameSnapshot:
    score: int
    high_score: int
    paused: bool
    game_over: bool


class GameController:
    """Owns game rules, timing, collisions, scoring, and callbacks to the UI layer."""

    def __init__(
        self,
        score_manager: ScoreManager,
        on_food_eaten: FoodCallback | None = None,
        on_score_changed: ScoreCallback | None = None,
        on_pause_changed: PauseCallback | None = None,
        on_game_over: GameOverCallback | None = None,
    ) -> None:
        self.score_manager = score_manager
        self.on_food_eaten = on_food_eaten
        self.on_score_changed = on_score_changed
        self.on_pause_changed = on_pause_changed
        self.on_game_over = on_game_over

        self.cols = settings.BOARD_COLS
        self.rows = settings.BOARD_ROWS
        self.rng = random.Random()
        self.snake = Snake(start=(self.cols // 2, self.rows // 2), length=settings.START_LENGTH)
        self.food = Food()

        self.score = 0
        self.high_score = self.score_manager.high_score
        self.is_paused = False
        self.is_game_over = False
        self.is_boosting = False
        self.walls: set[GridPos] = set()
        self.elapsed_time = 0.0
        self.accumulator = 0.0
        self.food.respawn(self.cols, self.rows, self.snake.occupied, self.rng)

    @property
    def move_interval(self) -> float:
        # Base speed scales with score; boost temporarily reduces the interval further.
        speed_boosts = self.score // settings.SPEED_SCORE_STEP
        base = max(settings.BASE_MOVE_INTERVAL - speed_boosts * settings.SPEED_STEP, settings.MIN_MOVE_INTERVAL)
        return max(base * settings.BOOST_INTERVAL_FACTOR, settings.MIN_MOVE_INTERVAL) if self.is_boosting else base

    def set_boost(self, active: bool) -> None:
        """Enable or disable speed boost (hold Space / Shift on PC)."""
        self.is_boosting = active

    @property
    def interpolation_alpha(self) -> float:
        if self.is_game_over:
            return 1.0
        return min(1.0, self.accumulator / self.move_interval)

    def snapshot(self) -> GameSnapshot:
        return GameSnapshot(
            score=self.score,
            high_score=self.high_score,
            paused=self.is_paused,
            game_over=self.is_game_over,
        )

    def start_new_game(self) -> None:
        """Reset transient match state while preserving stored high score data."""
        self.score = 0
        self.high_score = self.score_manager.load()
        self.is_paused = False
        self.is_game_over = False
        self.is_boosting = False
        self.elapsed_time = 0.0
        self.accumulator = 0.0
        self.snake.reset((self.cols // 2, self.rows // 2), settings.START_LENGTH)
        self.walls = self._generate_walls()
        self.food.respawn(self.cols, self.rows, self.snake.occupied | self.walls, self.rng)
        self._notify_score_changed()
        self._notify_pause_changed()

    def request_direction(self, direction_name: str) -> bool:
        """Forward direction requests to Snake unless game input is currently blocked."""
        if self.is_paused or self.is_game_over:
            return False
        return self.snake.request_direction(direction_name)

    def pause(self) -> None:
        if self.is_game_over:
            return
        self.is_paused = True
        self._notify_pause_changed()

    def resume(self) -> None:
        if self.is_game_over:
            return
        self.is_paused = False
        self._notify_pause_changed()

    def toggle_pause(self) -> None:
        if self.is_paused:
            self.resume()
        else:
            self.pause()

    def update(self, dt: float) -> None:
        if self.is_paused or self.is_game_over:
            return

        # Fixed-step simulation keeps movement deterministic even if frame time fluctuates.
        self.elapsed_time += dt
        self.accumulator += dt
        while self.accumulator >= self.move_interval:
            self.accumulator -= self.move_interval
            self._step()
            if self.is_game_over:
                break

    def _step(self) -> None:
        """Process one gameplay tick: movement, collision checks, and food handling."""
        raw_next_head = self.snake.next_head()

        # Wrap around all edges — crossing any side brings you out the other side
        next_head = (raw_next_head[0] % self.cols, raw_next_head[1] % self.rows)
        will_grow = next_head == self.food.position

        # Wall collision — touching a wooden wall is fatal
        if next_head in self.walls:
            self._set_game_over()
            return

        if is_self_collision(next_head, self.snake.occupied, self.snake.tail, will_grow):
            self._set_game_over()
            return

        # Pass the (possibly wrapped) head position to the snake
        self.snake.move(grow=will_grow, forced_head=next_head)

        if will_grow:
            self.score += settings.FOOD_SCORE
            self.high_score = self.score_manager.save(self.score)
            self.food.respawn(self.cols, self.rows, self.snake.occupied | self.walls, self.rng)
            self._notify_score_changed()
            if self.on_food_eaten is not None:
                self.on_food_eaten(self.food.position, self.score)

    def _generate_walls(self) -> set[GridPos]:
        """Randomly place wall clusters on the board, keeping spawn zone clear."""
        start_x = self.cols // 2
        start_y = self.rows // 2
        radius = settings.WALL_SAFE_RADIUS

        # Build safe zone around snake start position
        safe: set[GridPos] = {
            (x, y)
            for x in range(max(0, start_x - radius), min(self.cols, start_x + radius + 1))
            for y in range(max(0, start_y - radius), min(self.rows, start_y + radius + 1))
        }
        safe |= self.snake.occupied

        walls: set[GridPos] = set()
        attempts = 0
        while len(walls) < settings.WALL_COUNT and attempts < 600:
            attempts += 1
            # Seed tile — avoid board border so snake always has an escape
            sx = self.rng.randint(1, self.cols - 2)
            sy = self.rng.randint(1, self.rows - 2)
            if (sx, sy) in safe or (sx, sy) in walls:
                continue
            # Grow a small cluster of 2–4 tiles
            cluster: set[GridPos] = {(sx, sy)}
            for _ in range(self.rng.randint(1, 3)):
                adjacent = [
                    (cx + dx, cy + dy)
                    for cx, cy in cluster
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                    if 1 <= cx + dx < self.cols - 1
                    and 1 <= cy + dy < self.rows - 1
                    and (cx + dx, cy + dy) not in safe
                    and (cx + dx, cy + dy) not in cluster
                ]
                if not adjacent:
                    break
                cluster.add(self.rng.choice(adjacent))
            walls |= cluster

        return walls

    def _set_game_over(self) -> None:
        """Freeze gameplay and persist score once a fatal collision is detected."""
        self.is_game_over = True
        self.high_score = self.score_manager.save(self.score)
        if self.on_game_over is not None:
            self.on_game_over(self.score, self.high_score)

    def _notify_score_changed(self) -> None:
        if self.on_score_changed is not None:
            self.on_score_changed(self.score, self.high_score)

    def _notify_pause_changed(self) -> None:
        if self.on_pause_changed is not None:
            self.on_pause_changed(self.is_paused)