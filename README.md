# Snake Game

A production-style Snake game built with Python and Kivy, structured for Android packaging with Buildozer.

## Folder Structure

```text
snake_game/
├── main.py
├── ads_manager.py
├── game/
│   ├── collision.py
│   ├── food.py
│   ├── game_controller.py
│   ├── settings.py
│   └── snake.py
├── ui/
│   ├── game_over_screen.kv
│   ├── game_screen.kv
│   └── menu_screen.kv
├── assets/
│   ├── images/
│   │   ├── background.png
│   │   ├── food.png
│   │   ├── snake_body.png
│   │   └── snake_head.png
│   └── sounds/
│       ├── click.wav
│       ├── eat.wav
│       └── game_over.wav
├── utils/
│   ├── score_manager.py
│   └── storage.py
├── buildozer.spec
└── README.md
```

## Features

- Grid-based smooth snake movement with 60 FPS rendering
- Swipe controls for mobile devices
- Direction reversal protection
- Score and locally persisted high score
- Difficulty ramp based on score
- Pause, resume, restart, and game over flow
- Particle burst when food is eaten
- Audio hooks for click, eat, and game over events
- Android-ready Buildozer configuration
- Monetization-ready ad manager stubs for banner and rewarded ads

## Run Locally

1. Create and activate a Python 3.13 virtual environment. Avoid Python 3.14 for now because Kivy Windows wheels are not available there in this setup.
2. Install Kivy:

```bash
pip install kivy==2.3.1
```

3. Start the game:

```bash
python main.py
```

## Build Android APK With Buildozer

Buildozer is typically run inside Linux or WSL. On Windows, use WSL2 or a Linux machine.

1. Install system dependencies for Buildozer and Android SDK tooling.
2. Open the project directory.
3. Run:

```bash
buildozer android debug
```

4. The generated APK will be available under the `bin/` directory.

To build a release package:

```bash
buildozer android release
```

## Google Play Store Publishing Checklist

1. Replace placeholder art and sound assets with production assets.
2. Set your final package domain and app signing configuration in `buildozer.spec`.
3. Prepare store listing assets: icon, screenshots, feature graphic, privacy policy.
4. Integrate real AdMob SDK logic into `ads_manager.py` if monetization is required.
5. Generate a signed AAB or APK for release.
6. Upload the release build in the Google Play Console.
7. Complete content rating, target audience, data safety, and app access forms.

## Notes

- The repository includes placeholder media files so the asset pipeline is ready.
- The game gracefully falls back to simple shapes if any asset fails to load.
- High score data is stored in Kivy's user data directory on desktop and Android.
