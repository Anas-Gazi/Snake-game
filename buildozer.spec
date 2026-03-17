[app]
title = Snake Game
package.name = snakegame
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,wav,json,md
version = 1.0.0

requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 0

android.api = 33
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET,VIBRATE
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.enable_androidx = True

presplash.filename = assets/images/background.png
icon.filename = assets/images/food.png

[buildozer]
log_level = 2
warn_on_root = 1