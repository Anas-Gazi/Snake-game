"""Scoring system with combo multiplier."""
from __future__ import annotations

from typing import Callable

from config import constants


class ScoringSystem:
    """Manages score, combo multiplier, and XP rewards."""

    def __init__(self, progression_system) -> None:
        """Initialize scoring system.
        
        Args:
            progression_system: ProgressionSystem instance.
        """
        self.progression_system = progression_system
        self.score = 0
        self.high_score = 0
        self.combo_level = 0
        self.combo_timer = 0.0
        self.on_score_changed: Callable[[int, int], None] | None = None
        self.on_combo_changed: Callable[[int], None] | None = None

    def add_score(self, base_points: int, food_type: str = "normal") -> None:
        """Add score with combo multiplier.
        
        Args:
            base_points: Base points to add.
            food_type: Type of food eaten ("normal", "bonus", "poison").
        """
        # Calculate multiplier
        multiplier = 1.0 + (self.combo_level * constants.COMBO_MULTIPLIER_INCREMENT)
        multiplier = min(multiplier, 1.0 + (constants.MAX_COMBO_LEVEL * constants.COMBO_MULTIPLIER_INCREMENT))

        # Handle different food types
        if food_type == "bonus":
            points = int(base_points * constants.XP_MULTIPLIER_BONUS * multiplier)
        elif food_type == "poison":
            points = base_points  # No multiplier for poison
        else:
            points = int(base_points * multiplier)

        self.score += points
        self.high_score = max(self.high_score, self.score)

        # Reset combo on poison
        if food_type != "poison":
            self.combo_timer = constants.COMBO_TIMEOUT
            self.combo_level = min(self.combo_level + 1, constants.MAX_COMBO_LEVEL)
            if self.on_combo_changed:
                self.on_combo_changed(self.combo_level)

        # Add XP
        xp_amount = int(base_points * (self.progression_system.level / 10))
        if food_type == "bonus":
            xp_amount = int(xp_amount * constants.XP_MULTIPLIER_BONUS)
        self.progression_system.add_xp(max(1, xp_amount))

        if self.on_score_changed:
            self.on_score_changed(self.score, self.high_score)

    def update(self, dt: float) -> bool:
        """Update combo timer.
        
        Args:
            dt: Delta time.
            
        Returns:
            True if combo was broken.
        """
        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                old_combo = self.combo_level
                self.combo_level = 0
                if self.on_combo_changed:
                    self.on_combo_changed(0)
                return old_combo > 0
        return False

    def reset(self) -> None:
        """Reset score for new game."""
        self.score = 0
        self.combo_level = 0
        self.combo_timer = 0.0
        if self.on_score_changed:
            self.on_score_changed(0, self.high_score)
