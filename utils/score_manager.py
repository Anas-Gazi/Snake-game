from __future__ import annotations

from game import settings
from utils.storage import load_json, save_json


class ScoreManager:
    def __init__(self) -> None:
        self.high_score = 0
        self.load()

    def load(self) -> int:
        payload = load_json(settings.SCORE_STORAGE_FILE, {settings.HIGH_SCORE_KEY: 0})
        self.high_score = int(payload.get(settings.HIGH_SCORE_KEY, 0))
        return self.high_score

    def save(self, score: int) -> int:
        self.high_score = max(self.high_score, score)
        save_json(settings.SCORE_STORAGE_FILE, {settings.HIGH_SCORE_KEY: self.high_score})
        return self.high_score

    def reset(self) -> None:
        self.high_score = 0
        save_json(settings.SCORE_STORAGE_FILE, {settings.HIGH_SCORE_KEY: 0})