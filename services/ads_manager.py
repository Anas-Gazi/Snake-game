"""Ad integration manager (stub for production integration)."""
from __future__ import annotations

from typing import Callable


class AdsManager:
    """Manages ad loading and display (production-ready but stubbed)."""

    def __init__(self, save_manager) -> None:
        """Initialize ads manager.
        
        Args:
            save_manager: SaveManager instance.
        """
        self.save_manager = save_manager
        self.banner_loaded = False
        self.rewarded_loaded = False
        self.initialized = False
        self.test_mode = True  # For testing without real ads
        self.on_rewarded_complete: Callable[[bool], None] | None = None

    def initialize(self, test_mode: bool = True) -> None:
        """Initialize AdMob (stub).
        
        In production, this would initialize the Google Mobile Ads SDK.
        
        Args:
            test_mode: Whether to use test device IDs.
        """
        self.test_mode = test_mode
        self.initialized = True
        print(f"[AdsManager] Initialized (test_mode={test_mode})")

    def load_banner(self) -> None:
        """Load banner ad (stub).
        
        In production, this would call the AdMob banner load.
        """
        if not self.initialized:
            self.initialize()
        self.banner_loaded = True
        print("[AdsManager] Banner loaded")

    def show_banner(self) -> None:
        """Show banner ad (stub)."""
        if not self.banner_loaded:
            self.load_banner()
        print("[AdsManager] Showing banner")

    def hide_banner(self) -> None:
        """Hide banner ad (stub)."""
        print("[AdsManager] Hiding banner")

    def load_rewarded(self) -> None:
        """Load rewarded ad (stub).
        
        In production, this would load an AdMob rewarded ad.
        """
        if not self.initialized:
            self.initialize()
        self.rewarded_loaded = True
        print("[AdsManager] Rewarded ad loaded")

    def show_rewarded(self) -> bool:
        """Show rewarded ad and wait for completion (stub).
        
        In production, this would show the rewarded ad and return True
        if user watched it completely.
        
        Returns:
            True if user completed the ad.
        """
        if not self.rewarded_loaded:
            self.load_rewarded()

        # Stub: always return True for testing
        print("[AdsManager] Showing rewarded ad (stubbed - auto-complete)")
        if self.on_rewarded_complete:
            self.on_rewarded_complete(True)
        return True

    def show_interstitial(self) -> None:
        """Show interstitial ad (stub).
        
        In production, this would show between-level or after-game-over ads.
        """
        if not self.initialized:
            self.initialize()
        print("[AdsManager] Showing interstitial ad")

    def should_show_ads(self) -> bool:
        """Check if ads should be shown (respects ad removal setting)."""
        return not self.save_manager.get_nested("settings.ads_removed", False)

    def remove_ads(self) -> None:
        """Mark ads as removed (in-app purchase stub)."""
        self.save_manager.set_nested("settings.ads_removed", True)
        self.save_manager.save()
        print("[AdsManager] Ads removed (user purchase)")
