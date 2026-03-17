from __future__ import annotations

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
UI_DIR = ROOT_DIR / "ui"

APP_TITLE = "Snake Game"
TARGET_FPS = 60

BOARD_COLS = 20
BOARD_ROWS = 30
START_LENGTH = 4

BASE_MOVE_INTERVAL = 0.18
MIN_MOVE_INTERVAL = 0.07
BOOST_INTERVAL_FACTOR = 0.40   # boost multiplies move_interval by this factor
SPEED_STEP = 0.01
SPEED_SCORE_STEP = 4

FOOD_SCORE = 10
TOUCH_SWIPE_THRESHOLD = 24
PARTICLE_COUNT = 10
PARTICLE_LIFETIME = 0.28

WALL_COUNT = 20          # total wall tiles placed per game
WALL_SAFE_RADIUS = 12    # cells around the snake spawn kept clear of walls

BOARD_BACKGROUND_COLOR = (0.05, 0.09, 0.11, 1)
GRID_LINE_COLOR = (1, 1, 1, 0.04)
SNAKE_HEAD_COLOR = (0.18, 0.82, 0.38, 1)
SNAKE_BODY_COLOR = (0.13, 0.62, 0.31, 1)
FOOD_COLOR = (0.96, 0.34, 0.26, 1)
PARTICLE_COLOR = (1, 0.78, 0.31, 0.95)
TEXT_COLOR = (0.96, 0.97, 0.98, 1)
PANEL_COLOR = (0.09, 0.13, 0.16, 0.94)
ACCENT_COLOR = (0.17, 0.72, 0.53, 1)
ACCENT_ALT_COLOR = (0.94, 0.45, 0.22, 1)
WALL_COLOR = (0.42, 0.27, 0.11, 1)
WALL_GRAIN_COLOR = (0.58, 0.38, 0.16, 1)

WINDOW_MIN_WIDTH = 420
WINDOW_MIN_HEIGHT = 760

SCORE_STORAGE_FILE = "save_data.json"
HIGH_SCORE_KEY = "high_score"

SNAKE_HEAD_IMAGE = str(IMAGES_DIR / "snake_head.png")
SNAKE_BODY_IMAGE = str(IMAGES_DIR / "snake_body.png")
FOOD_IMAGE = str(IMAGES_DIR / "food.png")
BACKGROUND_IMAGE = str(IMAGES_DIR / "background.png")
WALL_IMAGE = str(IMAGES_DIR / "wall.png")

EAT_SOUND = str(SOUNDS_DIR / "eat.wav")
GAME_OVER_SOUND = str(SOUNDS_DIR / "game_over.wav")
CLICK_SOUND = str(SOUNDS_DIR / "click.wav")

KV_FILES = [
    str(UI_DIR / "menu_screen.kv"),
    str(UI_DIR / "game_screen.kv"),
    str(UI_DIR / "game_over_screen.kv"),
]


def usable_asset(path: str) -> str | None:
    asset_path = Path(path)
    if asset_path.exists() and asset_path.stat().st_size > 0:
        return str(asset_path)
    return None