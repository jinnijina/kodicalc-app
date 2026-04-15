[app]

title = Kodi Calc
package.name = timbercalc
package.domain = org.femunu12

source.dir = .
source.include_exts = py,png,jpg,kv

version = 0.1

requirements = python3,kivy,kivymd,pillow

icon.filename = icon.png

fullscreen = 0

[buildozer]

log_level = 2
warn_on_root = 1

[app:android]

android.api = 31
android.minapi = 21
android.arch = arm64-v8a
