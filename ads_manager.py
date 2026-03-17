from __future__ import annotations


class AdsManager:
    """Ad integration stub for future Android monetization work."""

    def __init__(self) -> None:
        self.banner_loaded = False
        self.rewarded_loaded = False
        self.initialized = False

    def initialize(self, test_mode: bool = True) -> None:
        self.initialized = True

    def load_banner(self) -> None:
        self.banner_loaded = True

    def show_banner(self) -> None:
        if not self.initialized:
            self.initialize()

    def hide_banner(self) -> None:
        return None

    def load_rewarded(self) -> None:
        self.rewarded_loaded = True

    def show_rewarded(self) -> bool:
        return self.rewarded_loaded