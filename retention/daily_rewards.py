"""Retention systems: daily rewards and streak tracking."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Callable

from config import constants


class DailyRewardSystem:
    """Manages daily login rewards and streak bonuses."""

    def __init__(self, save_manager) -> None:
        """Initialize daily reward system.
        
        Args:
            save_manager: SaveManager instance.
        """
        self.save_manager = save_manager
        self.on_reward_claimed: Callable[[int, int], None] | None = None  # (reward_amount, new_streak)

    def can_claim_reward(self) -> bool:
        """Check if player can claim today's reward.
        
        Returns:
            True if reward can be claimed.
        """
        last_claimed = self.save_manager.get_nested("daily_rewards.last_claimed")
        if last_claimed is None:
            return True

        try:
            last_date = datetime.fromisoformat(last_claimed).date()
            today = datetime.now().date()
            return last_date != today
        except (ValueError, TypeError):
            return True

    def claim_reward(self) -> tuple[int, int]:
        """Claim today's daily reward.
        
        Returns:
            Tuple of (reward_amount, current_streak).
        """
        if not self.can_claim_reward():
            return 0, self.get_streak()

        # Check streak continuity
        last_claimed = self.save_manager.get_nested("daily_rewards.last_claimed")
        current_streak = self.get_streak()

        if last_claimed is None:
            # First time
            new_streak = 1
        else:
            try:
                last_date = datetime.fromisoformat(last_claimed).date()
                today = datetime.now().date()
                days_diff = (today - last_date).days

                if days_diff == 1:
                    # Consecutive day
                    new_streak = min(current_streak + 1, constants.MAX_STREAK)
                else:
                    # Streak broken
                    new_streak = 1
            except (ValueError, TypeError):
                new_streak = 1

        # Calculate reward
        reward_amount = constants.DAILY_REWARD_BASE + (new_streak - 1) * constants.DAILY_REWARD_STREAK_BONUS
        coins = self.save_manager.get_nested("player.coins", 0)
        self.save_manager.set_nested("player.coins", coins + reward_amount)

        # Update daily rewards data
        self.save_manager.set_nested("daily_rewards.last_claimed", datetime.now().isoformat())
        self.save_manager.set_nested("daily_rewards.streak", new_streak)
        self.save_manager.set_nested("daily_rewards.total_claimed", 
                                      self.save_manager.get_nested("daily_rewards.total_claimed", 0) + 1)
        self.save_manager.save()

        if self.on_reward_claimed:
            self.on_reward_claimed(reward_amount, new_streak)

        return reward_amount, new_streak

    def get_streak(self) -> int:
        """Get current login streak."""
        return self.save_manager.get_nested("daily_rewards.streak", 0)

    def get_days_until_reset(self) -> float:
        """Get hours until streak resets if not claimed.
        
        Returns:
            Hours remaining until streak reset.
        """
        last_claimed = self.save_manager.get_nested("daily_rewards.last_claimed")
        if last_claimed is None:
            return constants.STREAK_RESET_HOURS

        try:
            last_time = datetime.fromisoformat(last_claimed)
            reset_time = last_time + timedelta(hours=constants.STREAK_RESET_HOURS)
            time_diff = reset_time - datetime.now()
            return max(0, time_diff.total_seconds() / 3600)
        except (ValueError, TypeError):
            return constants.STREAK_RESET_HOURS


class ReviveSystem:
    """Manages rewarded ad-based revive system."""

    def __init__(self, save_manager) -> None:
        """Initialize revive system.
        
        Args:
            save_manager: SaveManager instance.
        """
        self.save_manager = save_manager
        self.revives_used_today = 0
        self.on_revive_used: Callable[[], None] | None = None

    def can_revive(self) -> bool:
        """Check if player can use a revive (ad-based).
        
        Returns:
            True if revive is available.
        """
        if self.save_manager.get_nested("settings.ads_removed"):
            # If ads are removed, no paid revives (cosmetic only)
            return False

        # Check daily limit
        return self.revives_used_today < constants.REWARDED_AD_REVIVE_LIMIT

    def use_revive(self) -> bool:
        """Use a revive (would show rewarded ad).
        
        Returns:
            True if revive was successfully used.
        """
        if not self.can_revive():
            return False

        self.revives_used_today += 1

        if self.on_revive_used:
            self.on_revive_used()

        return True

    def reset_daily_limit(self) -> None:
        """Reset revives count (called daily)."""
        self.revives_used_today = 0

    def get_revives_remaining(self) -> int:
        """Get revives remaining today."""
        return max(0, constants.REWARDED_AD_REVIVE_LIMIT - self.revives_used_today)
