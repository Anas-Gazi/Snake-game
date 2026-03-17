"""Input handling with direction buffering."""
from __future__ import annotations

from collections import deque
from typing import Callable

from config import constants


class InputHandler:
    """Manages buffered input directions."""

    DIRECTION_VECTORS = {
        "up": (0, 1),
        "down": (0, -1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    def __init__(self) -> None:
        """Initialize input handler."""
        self.direction_buffer: deque[str] = deque(maxlen=constants.DIRECTION_BUFFER_SIZE)
        self.current_direction = "right"
        self.pending_direction = "right"
        self.on_direction_requested: Callable[[str], None] | None = None

    def request_direction(self, direction: str) -> bool:
        """Request a direction change.
        
        Args:
            direction: Direction name ("up", "down", "left", "right").
            
        Returns:
            True if direction was buffered.
        """
        if direction not in self.DIRECTION_VECTORS:
            return False

        # Prevent 180-degree reversal
        if self._is_opposite(self.current_direction, direction):
            return False

        self.direction_buffer.append(direction)
        if self.on_direction_requested:
            self.on_direction_requested(direction)
        return True

    def get_buffered_direction(self) -> str | None:
        """Get next buffered direction.
        
        Returns:
            Next direction to execute, or None if buffer empty.
        """
        if self.direction_buffer:
            direction = self.direction_buffer.popleft()
            # Validate it's not a reversal
            if self._is_opposite(self.current_direction, direction):
                # Skip this input
                return self.get_buffered_direction()
            self.pending_direction = direction
            return direction
        return None

    def apply_direction(self) -> None:
        """Apply the pending direction as current."""
        self.current_direction = self.pending_direction

    def clear_buffer(self) -> None:
        """Clear the input buffer."""
        self.direction_buffer.clear()

    def _is_opposite(self, current: str, requested: str) -> bool:
        """Check if requested direction is opposite to current."""
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        return opposites.get(current) == requested

    def reset(self) -> None:
        """Reset input state."""
        self.clear_buffer()
        self.current_direction = "right"
        self.pending_direction = "right"
