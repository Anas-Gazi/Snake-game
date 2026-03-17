"""Leaderboard systems (local and global ready)."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from config import constants


class LocalLeaderboard:
    """Local leaderboard for high scores."""

    def __init__(self, save_manager) -> None:
        """Initialize local leaderboard.
        
        Args:
            save_manager: SaveManager instance.
        """
        self.save_manager = save_manager
        self.leaderboard_file = Path(save_manager.save_dir) / constants.LEADERBOARD_FILENAME
        self.entries = []
        self.load()

    def load(self) -> None:
        """Load leaderboard from file."""
        if self.leaderboard_file.exists():
            try:
                with open(self.leaderboard_file, "r") as f:
                    self.entries = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.entries = []
        else:
            self.entries = []

    def save(self) -> None:
        """Persist leaderboard to file."""
        try:
            with open(self.leaderboard_file, "w") as f:
                json.dump(self.entries, f, indent=2)
        except IOError as e:
            print(f"Failed to save leaderboard: {e}")

    def submit_score(self, player_name: str, mode: str, score: int) -> int:
        """Submit a score to the leaderboard.
        
        Args:
            player_name: Player name.
            mode: Game mode.
            score: Score achieved.
            
        Returns:
            Leaderboard position (1-indexed), or -1 if not ranked.
        """
        entry = {
            "player": player_name,
            "mode": mode,
            "score": score,
            "timestamp": datetime.now().isoformat(),
        }

        self.entries.append(entry)
        # Sort by score descending
        self.entries.sort(key=lambda x: x["score"], reverse=True)
        # Keep top 100
        self.entries = self.entries[:100]
        self.save()

        # Find position
        for i, e in enumerate(self.entries):
            if e["timestamp"] == entry["timestamp"]:
                return i + 1

        return -1

    def get_top_scores(self, mode: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        """Get top scores.
        
        Args:
            mode: Filter by mode, or None for all.
            limit: Maximum number of entries.
            
        Returns:
            List of score entries.
        """
        entries = [e for e in self.entries
                   if mode is None or e.get("mode") == mode]
        return entries[:limit]

    def get_player_rank(self, player_name: str, mode: str | None = None) -> int:
        """Get player's rank.
        
        Args:
            player_name: Player name.
            mode: Game mode, or None for all.
            
        Returns:
            Rank (1-indexed), or -1 if not ranked.
        """
        entries = [e for e in self.entries
                   if mode is None or e.get("mode") == mode]
        for i, e in enumerate(entries):
            if e.get("player") == player_name:
                return i + 1
        return -1

    def clear(self) -> None:
        """Clear leaderboard (test/admin only)."""
        self.entries = []
        self.save()


class GlobalLeaderboard:
    """Global leaderboard interface (Firebase-ready stub).
    
    This is structured for Firebase integration:
    - Uses async/await pattern hooks
    - Stores timestamps for ranking
    - Supports multiple modes
    - Ready for Firestore integration
    """

    def __init__(self, save_manager) -> None:
        """Initialize global leaderboard.
        
        Args:
            save_manager: SaveManager instance.
        """
        self.save_manager = save_manager
        self.is_synced = False
        self.entries = []
        self.user_rank = -1
        # In production: initialize Firebase

    def submit_score_async(self, player_name: str, mode: str, score: int) -> None:
        """Submit score to global leaderboard (async in production).
        
        In production, this would send to Firebase and get a callback.
        
        Args:
            player_name: Player name.
            mode: Game mode.
            score: Score achieved.
        """
        # Stub: In production, send to Firebase with callback
        print(f"[GlobalLeaderboard] Would submit to Firebase: {player_name} scored {score} in {mode}")

    def fetch_top_scores_async(self, mode: str, limit: int = 10) -> list[dict[str, Any]]:
        """Fetch top scores from global leaderboard.
        
        In production, this would be truly async with callbacks.
        
        Args:
            mode: Game mode.
            limit: Maximum entries.
            
        Returns:
            List of score entries from cache.
        """
        # Stub: In production, fetch from Firebase
        return self.entries[:limit]

    def fetch_player_rank_async(self, player_name: str, mode: str) -> int:
        """Fetch player's global rank.
        
        Args:
            player_name: Player name.
            mode: Game mode.
            
        Returns:
            Global rank, or -1 if unknown.
        """
        # Stub: In production, query Firebase
        return self.user_rank
